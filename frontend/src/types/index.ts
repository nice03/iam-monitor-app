// src/types/index.ts

// API 응답 타입 정의
export interface APIUserResponse {
  AccessKeyId: string;       // 액세스 키 ID
  LastUsedDate: string;      // 마지막 사용 일자
  UserId: string;           // 사용자 ID
  UserName: string;         // 사용자 이름
  AccessKeyAge?: string;     // 키 생성 후 경과 시간 (iam/users 응답에만 존재)
  AccessKeyCreateDate?: string; // 키 생성 일자 (iam/users 응답에만 존재)
  Status: string;  // Status 필드 추가
}

export interface APIResponse {
  users: APIUserResponse[];
}

export interface IAMUser {
  UserId: string;
  UserName: string;
  AccessKeyAge: string;
  AccessKeyCreateDate: string;
  LastUsedDate: string;
  username: string;
  arn: string;
  creation_date: string;
  mfa_enabled: boolean;
  console_access: boolean;
  last_console_login?: string;
  access_keys: AccessKey[];
  stack: string;
}

export interface AccessKey {
  key_id: string;
  status: string;
  created_date: string;
  last_used?: string;
}

export interface MonitoringCriteria {
  hours: number;
  stack?: string;
  mfa_required: boolean;
  check_inactive_keys: boolean;
}

// API 응답을 프론트엔드 형식으로 변환
export const transformAPIResponse = (apiUser: APIUserResponse): IAMUser => {
  return {
    UserId: apiUser.UserId,
    UserName: apiUser.UserName,
    // API 응답에 있는 경우 해당 값 사용, 없으면 빈 문자열
    AccessKeyAge: apiUser.AccessKeyAge || '',
    AccessKeyCreateDate: apiUser.AccessKeyCreateDate || '',
    LastUsedDate: apiUser.LastUsedDate,
    username: apiUser.UserName.toLowerCase(),
    arn: `arn:aws:iam::*:user/${apiUser.UserName}`,
    creation_date: apiUser.AccessKeyCreateDate || '',
    mfa_enabled: false,
    console_access: false,
    access_keys: [{
      key_id: apiUser.AccessKeyId,
      status: apiUser.Status,  // API에서 받은 상태값 사용
      created_date: apiUser.AccessKeyCreateDate || '',
      last_used: apiUser.LastUsedDate
    }],
    stack: ''
  };
};