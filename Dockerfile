# Versão python utilizada neste projeto
FROM python:3-alpine3.6

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

# installa a dependencia psycopg2
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /code/

# Instala os pacotes python utilizado no projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./backend/ /code/




