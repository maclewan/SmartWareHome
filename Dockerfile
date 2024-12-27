# syntax=docker/dockerfile:1
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir backend_app
WORKDIR /backend_app
RUN mkdir requirements
COPY requirements/local.txt /backend_app/requirements
COPY requirements/base.txt /backend_app/requirements
RUN pip install -r requirements/local.txt
RUN apt-get update && apt-get install -y bluez libbluetooth-dev
COPY . /backend_app
