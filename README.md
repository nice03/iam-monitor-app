# IAM Monitor - AWS IAM Access Key 모니터링

## 개요

이 애플리케이션은 AWS IAM 사용자 액세스 키를 모니터링하여 오래된 키와 미사용 키를 추적하여 보안 관리를 돕습니다.

> **참고**: 이 가이드는 M1 Mac에 minikube와 Docker가 설치되어 있다고 가정합니다.
<img width="1379" alt="스크린샷 2024-11-07 오후 6 09 00" src="https://github.com/user-attachments/assets/e83641a9-f1b3-4d97-84a0-e445cff9c150">

## 사전 준비 사항

- minikube (M1 Mac에 설치됨)
- Docker (M1 Mac에 설치됨)
- kubectl
- AWS 계정 및 자격증명 (Access Key, Secret Key)
- Node.js 16 이상
- npm 또는 yarn

## 프로젝트 구조

```plaintext
iam-monitor-app/
├── README.md
├── backend/                    # 백엔드 애플리케이션
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── controllers/
│       │   └── iam_controller.py
│       ├── services/
│       │   └── iam_service.py
│       ├── utils/
│       │   └── aws_utils.py
│       └── main.py
├── frontend/                   # 프론트엔드 애플리케이션
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── components/
│       │   ├── MonitoringForm.tsx
│       │   └── UserTable.tsx
│       ├── services/
│       ├── types/
│       │   └── index.ts
│       ├── App.tsx
│       ├── config.ts
│       └── index.tsx
├── deploy/                     # 배포 설정
│   └── minikube/
│       ├── iam-monitor-api-deployment.yaml
│       ├── iam-monitor-api-service.yaml
│       ├── iam-monitor-web-deployment.yaml
│       ├── iam-monitor-web-service.yaml
│       ├── iam-monitor-web-ingress.yml
│       └── secrets/
│           ├── README.md
│           ├── iam-monitor-api-secrets.yaml
│           └── iam-monitor-api-secrets.yaml.template
└── scripts/                    # 유틸리티 스크립트
    └── create-secrets.sh
```

## 설치 및 설정 가이드

### 1. AWS 자격증명 설정

AWS 자격증명을 환경 변수로 설정하여 시크릿을 생성합니다:

```bash
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_key_here"
```

### 2. 시크릿 생성

다음 스크립트를 실행하여 Kubernetes 시크릿을 생성합니다:

```bash
./scripts/create-secrets.sh
```

### 3. 애플리케이션 빌드 및 배포

#### Step 1: Minikube 시작

Minikube가 실행 중이 아니면 시작합니다:

```bash
minikube start
```

참고: 캐시된 이미지에 문제가 있는 경우 강제로 제거해야 할 수 있습니다.

#### Step 2: 네임스페이스 생성

배포를 위한 Kubernetes 네임스페이스를 생성합니다:

```bash
kubectl create ns musinsa
```

#### Step 3: 도커 이미지 빌드

Minikube 환경으로 도커 환경을 설정하고 백엔드와 프론트엔드의 도커 이미지를 빌드합니다:

```bash
eval $(minikube docker-env)
docker build -t iam-monitor-api:latest ./backend
docker build -t iam-monitor-web:latest ./frontend
```

#### Step 4: Minikube에 배포

배포 파일을 적용하여 Kubernetes에 리소스를 생성합니다:

```bash
kubectl apply -f deploy/minikube/
```

#### Step 5: 시크릿 적용

시크릿 설정을 적용합니다:

```bash
kubectl apply -f deploy/minikube/secrets
```

### 4. 서비스 접속

프론트엔드 서비스에 접속하려면 다음 명령어를 실행하여 URL을 확인합니다:

```bash
minikube service iam-monitor-web -n musinsa
```

명령어가 표시하는 URL을 사용하여 브라우저에서 애플리케이션에 접속할 수 있습니다.

## 기술 스택

### 백엔드

- Python
- Flask
- Boto3 (AWS SDK)

### 프론트엔드

- React
- TypeScript
- Tailwind CSS

### 인프라스트럭처

- Kubernetes (minikube)
- Docker
- Nginx

## 주의사항

- 시크릿 파일(`deploy/minikube/secrets/*.yaml`)은 절대 Git에 커밋하지 마세요.
- AWS 자격증명은 반드시 안전하게 관리하세요.
- Minikube를 사용하여 로컬에서 개발 환경을 테스트하세요.
- kubectl과 Kubernetes 버전이 호환되지 않는 문제가 발생하면 Minikube에서 권장하는 버전을 사용하세요.

