import datetime
from dateutil import tz
from botocore.exceptions import ClientError
from utils.aws_utils import calculate_age, format_datetime, is_key_older_than, is_key_unused_since

class IAMService:
    def __init__(self, aws_client):
        """
        IAM 서비스 클래스 초기화
        Args:
            aws_client: AWS IAM 클라이언트 인스턴스
        """
        self.aws_client = aws_client

    def get_last_used_info(self, user_name, access_key_id=None):
        """
        사용자의 액세스 키와 콘솔 마지막 사용 날짜 조회 및 통합
        Args:
            user_name (str): IAM 사용자 이름
            access_key_id (str): 액세스 키 ID
        Returns:
            str: 통합된 마지막 사용 정보 문자열
        """
        try:
            # 액세스 키 마지막 사용일 확인
            access_key_last_used = "Never"
            if access_key_id:
                response = self.aws_client.get_access_key_last_used(AccessKeyId=access_key_id)
                last_used = response.get('AccessKeyLastUsed', {}).get('LastUsedDate')
                if last_used:
                    access_key_last_used = format_datetime(last_used)

            # 콘솔 로그인 날짜 확인
            console_last_used = "Never"
            user_response = self.aws_client.get_user(UserName=user_name)
            console_last_login = user_response["User"].get("PasswordLastUsed")
            if console_last_login:
                console_last_used = format_datetime(console_last_login)

            # 통합된 사용 정보 생성
            if access_key_last_used == "Never" and console_last_used == "Never":
                return "Never"
            elif access_key_last_used == "Error" or console_last_used == "Error":
                return "Error"
            else:
                key_info = f"Access Key: {access_key_last_used}"
                console_info = f"Console: {console_last_used}"
                return f"{key_info} / {console_info}"

        except ClientError as e:
            print(f"Error fetching last used dates for user {user_name}: {e}")
            return "Error"

    def _get_user_key_info(self, user, key):
        """
        사용자의 액세스 키 정보를 가져오는 공통 메서드
        Args:
            user: IAM 사용자 정보
            key: 액세스 키 메타데이터
        Returns:
            dict: 사용자 및 키 정보를 포함한 딕셔너리
        """
        user_name = user["UserName"]
        create_date = key["CreateDate"]
        last_used = self.get_last_used_info(user_name, key["AccessKeyId"])
        days, hours = calculate_age(create_date)
        
        return {
            "UserId": user["UserId"],
            "UserName": user_name,
            "AccessKeyId": key["AccessKeyId"],
            "AccessKeyAge": f"{days} days, {hours} hours",
            "AccessKeyCreateDate": format_datetime(create_date),
            "LastUsedDate": last_used,  # 통합된 마지막 사용 정보
            "Status": key["Status"]
        }

    def get_iam_users_with_old_keys(self, age_in_hours):
        """
        지정된 시간 이내에 생성된 액세스 키를 가진 사용자 조회
        Args:
            age_in_hours (int): 입력받은 시간 (시간 단위)
        Returns:
            list: 조건에 맞는 키를 가진 사용자 목록
        """
        old_users = []
        paginator = self.aws_client.get_paginator("list_users")
        
        for page in paginator.paginate():
            for user in page["Users"]:
                user_name = user["UserName"]
                try:
                    access_keys = self.aws_client.list_access_keys(UserName=user_name)
                    print(f"\n사용자 {user_name}의 액세스 키 확인:")
                    print(f"보유 중인 키 개수: {len(access_keys['AccessKeyMetadata'])}")
                    
                    for key in access_keys["AccessKeyMetadata"]:
                        key_age = datetime.datetime.now(tz=tz.tzutc()) - key["CreateDate"]
                        hours_old = key_age.total_seconds() / 3600
                        
                        print(f"- 키 ID: {key['AccessKeyId']}")
                        print(f"  상태: {key['Status']}")
                        print(f"  생성일: {key['CreateDate']}")
                        print(f"  경과 시간: {hours_old:.2f}시간")
                        print(f"  기준 시간: {age_in_hours}시간")
                        
                        if is_key_older_than(key["CreateDate"], age_in_hours):
                            print("  => 조건에 맞음 (리스트에 포함)")
                            old_users.append(self._get_user_key_info(user, key))
                        else:
                            print("  => 조건에 맞지 않음 (제외)")
                            
                except ClientError as e:
                    print(f"Error getting access keys for user {user_name}: {e}")
                        
        return old_users

    def get_iam_users_with_unused_keys(self, days_unused):
        """
        지정된 일수동안 사용되지 않은 Active 상태의 액세스 키를 가진 사용자 조회
        Args:
            days_unused (int): 미사용 기준 일수
        Returns:
            list: 미사용 키를 가진 사용자 목록
        """
        cutoff_time = datetime.datetime.now(tz=tz.tzutc()) - datetime.timedelta(days=days_unused)
        unused_users = []
        paginator = self.aws_client.get_paginator("list_users")
        
        for page in paginator.paginate():
            for user in page["Users"]:
                user_name = user["UserName"]
                try:
                    access_keys = self.aws_client.list_access_keys(UserName=user_name)
                    
                    for key in access_keys["AccessKeyMetadata"]:
                        if key["Status"] == "Active":
                            # 키의 생성 날짜와 마지막 사용 정보 가져오기
                            create_date = key["CreateDate"]
                            last_used_info = self.get_last_used_info(user_name, key["AccessKeyId"])
                            
                            # 마지막 사용 정보에서 액세스 키 사용일 추출
                            access_key_date = "Never"
                            if "Access Key:" in last_used_info:
                                access_key_part = last_used_info.split(" / ")[0]
                                access_key_date = access_key_part.replace("Access Key: ", "")
                            
                            if access_key_date == "Never":
                                # 생성된 지 days_unused일 이상 지난 키만 포함
                                if datetime.datetime.now(tz=tz.tzutc()) - create_date >= datetime.timedelta(days=days_unused):
                                    unused_users.append(self._get_user_key_info(user, key))
                            else:
                                try:
                                    # 마지막 사용일이 cutoff_time보다 오래된 경우 포함
                                    last_used_datetime = datetime.datetime.strptime(access_key_date, "%Y-%m-%d %H:%M:%S %Z")
                                    last_used_datetime = last_used_datetime.replace(tzinfo=tz.tzutc())
                                    if last_used_datetime <= cutoff_time:
                                        unused_users.append(self._get_user_key_info(user, key))
                                except ValueError as e:
                                    print(f"Error parsing last used date for key {key['AccessKeyId']}: {e}")
                                    
                except ClientError as e:
                    print(f"Error getting access keys for user {user_name}: {e}")
                            
        return unused_users