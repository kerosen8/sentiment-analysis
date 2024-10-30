FROM python:3.10

RUN apt update \
    && apt install -y mc \
    && apt install -y vim

ENV PYTHONDOWNRITEBYTEDECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /opt/src
WORKDIR /opt/src

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src .

EXPOSE 800
