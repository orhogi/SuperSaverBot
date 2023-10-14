FROM python:3.11-alpine
LABEL authors="Rozievich"

WORKDIR /apps
COPY . /apps

RUN pip install -r requirements.txt
