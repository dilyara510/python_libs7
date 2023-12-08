# Используйте официальный образ Python
FROM python:3.12

# Установите рабочую директорию в контейнере
WORKDIR /usr/src/app

# Установите переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установите зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте проект
COPY . .
