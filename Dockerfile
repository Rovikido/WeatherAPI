# pull the official docker image
FROM python:3.10-slim-buster

LABEL MAINTAINER="Oleh Sinkevych oleh.sinkevych@lnu.edu.ua"

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set work directory
WORKDIR /app

# upgrade pip
RUN /opt/venv/bin/python3 -m pip install --upgrade pip

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . /app

EXPOSE 8000