FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

COPY .. .

CMD python manage.py runserver 0.0.0.0:8000
