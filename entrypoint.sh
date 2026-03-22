#!/bin/sh
set -e

python manage.py migrate

python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if username and password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Суперпользователь создан.")
else:
    print("Суперпользователь уже существует или переменные окружения не заданы.")
PY

python manage.py runserver 0.0.0.0:8000
