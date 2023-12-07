FROM python:3.10.13

# Python 3.10.13 이미지 상에 Django를 pip를 통해 설치합니다.
RUN pip3 install django

# 작업 디렉토리를 /django 설정합니다.
WORKDIR /django

# 현재 Dockerfile이 위치한  디렉토리의 모든 파일을 /finalDjango 디렉토리로 복사합니다.
COPY . .

# manage.py를 실행할 수 있는 디렉토리에서 Django 서버를 실행합니다.
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8321"]

# Django 서버의 포트를 8000으로 지정하였으므로 Docker 컨테이너도 8000 포트를 열어줍니다.
EXPOSE 8321
