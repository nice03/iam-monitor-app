import datetime
from dateutil import tz

def get_aws_client(service_name):
    """
    AWS 서비스 클라이언트 생성
    Args:
        service_name (str): AWS 서비스 이름 (예: 'iam', 's3' 등)
    Returns:
        boto3.client: AWS 서비스 클라이언트 인스턴스
    """
    import boto3
    return boto3.client(service_name)

def calculate_age(create_date):
    """
    생성 날짜로부터 현재까지의 경과 시간 계산
    Args:
        create_date (datetime): 생성 날짜
    Returns:
        tuple: (경과 일수, 경과 시간)
    """
    now = datetime.datetime.now(tz=tz.tzutc())
    age = now - create_date
    days = age.days
    hours = age.seconds // 3600
    return days, hours

def format_datetime(dt):
    """
    날짜/시간을 지정된 형식의 문자열로 변환
    Args:
        dt (datetime): 변환할 날짜/시간
    Returns:
        str: "YYYY-MM-DD HH:MM:SS TZ" 형식의 문자열
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S %Z")

def is_key_older_than(create_date, target_hours):
    """
    액세스 키가 입력받은 N시간 전에 생성되었는지 확인
    Args:
        create_date (datetime): 키 생성 일시
        target_hours (int): 기준이 되는 시간 (예: 2시간이면 2시간 전에 생성된 키를 찾음)
    Returns:
        bool: N시간 전에 생성된 키면 True
    예시:
        N=2시간일 때:
        - 1시간 전 생성 키 -> False (아직 2시간 안됨)
        - 2시간 전 생성 키 -> True (정확히 2시간 전)
        - 3시간 전 생성 키 -> True (2시간 이상 지남)
    """
    now = datetime.datetime.now(tz=tz.tzutc())
    age = now - create_date
    hours_old = age.total_seconds() / 3600
    
    # N시간 전에 생성된 키인지 확인
    return hours_old >= target_hours


def is_key_unused_since(last_used_date, cutoff_time):
    """
    마지막 사용 일시가 기준 시간보다 오래되었는지 확인
    Args:
        last_used_date (str): "YYYY-MM-DD HH:MM:SS TZ" 형식의 마지막 사용 일시
        cutoff_time (datetime): 기준이 되는 날짜/시간
    Returns:
        bool: 마지막 사용일이 기준 시간보다 오래되었으면 True
    """
    # 문자열을 datetime 객체로 변환
    last_used_date = datetime.datetime.strptime(last_used_date, "%Y-%m-%d %H:%M:%S %Z")
    # 시간대 정보 추가 (UTC)
    last_used_date = last_used_date.replace(tzinfo=tz.tzutc())
    # 기준 시간과 비교
    return last_used_date < cutoff_time