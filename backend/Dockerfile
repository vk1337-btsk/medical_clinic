FROM python:3.11-slim
LABEL authors="Valera K."

WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get clean

COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD python manage.py migrate \
    && python manage.py collectstatic --no-input \
    && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --log-level info

COPY . .