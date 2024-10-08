FROM python:3.8-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add libffi-dev zlib-dev jpeg-dev postgresql-dev gcc python3-dev musl-dev openssl

WORKDIR /attendance_django

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY server.crt /etc/ssl/certs/server.crt
COPY server.key /etc/ssl/private/server.key
