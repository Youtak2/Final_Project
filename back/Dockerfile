FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# requirements.txt는 이미 back 폴더 안에 있으니까 상대 경로로 복사
COPY requirements.txt .
RUN pip install -r requirements.txt

# 전체 백엔드 소스 복사
COPY . .

# gunicorn으로 Django 실행
CMD ["gunicorn", "crud.wsgi:application", "--bind", "0.0.0.0:8000"]
