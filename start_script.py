
import os


# 사용자 입력받아서 알맞은 행동하도록 세팅하기
os.system("docker-compose up --build")
os.system("docker-compose -f docker-compose.dev.yml up")
os.system("docker-compose exec web python manage.py migrate")