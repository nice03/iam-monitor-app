# docker/frontend.Dockerfile
FROM node:16-alpine as builder

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 파일 복사 및 의존성 설치
COPY package*.json ./
RUN npm install

# 소스 코드 복사
COPY . ./

# TypeScript 컴파일 및 빌드
RUN npm run build

# 프로덕션 환경을 위한 Nginx 설정
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]