#!/bin/bash
# scripts/create-secrets.sh

# 환경 변수가 설정되어 있는지 확인
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "Error: AWS credentials not set in environment variables"
    echo "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
    exit 1
fi

# secrets 디렉토리 생성
SECRETS_DIR="deploy/minikube/secrets"
mkdir -p $SECRETS_DIR

# base64 인코딩
ACCESS_KEY=$(echo -n "$AWS_ACCESS_KEY_ID" | base64)
SECRET_KEY=$(echo -n "$AWS_SECRET_ACCESS_KEY" | base64)

# 템플릿으로부터 secrets.yaml 생성
cat $SECRETS_DIR/iam-monitor-api-secrets.yaml.template | \
sed "s|\${AWS_ACCESS_KEY_ID_BASE64}|$ACCESS_KEY|g" | \
sed "s|\${AWS_SECRET_ACCESS_KEY_BASE64}|$SECRET_KEY|g" \
> $SECRETS_DIR/iam-monitor-api-secrets.yaml

echo "Secrets file created at $SECRETS_DIR/iam-monitor-api-secrets.yaml"
