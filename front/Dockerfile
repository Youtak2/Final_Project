FROM node:18-alpine AS build-stage

WORKDIR /app

# 🔽 1. 패키지 파일 복사
COPY package*.json ./

# 🔽 2. 의존성 설치
RUN npm install

# 🔽 3. 전체 소스 복사 (현재 front 폴더 기준)
COPY . ./

# 🔽 4. 빌드
RUN npm run build