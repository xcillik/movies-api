# syntax=docker/dockerfile:1
FROM python:3.10-slim-bullseye

RUN apt update -y
RUN pip3 install --upgrade pip

WORKDIR /root/movies-api

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
# COPY . .

WORKDIR /root/movies-api/app
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
