FROM python:3.9.6-alpine

RUN pip install --upgrade pip

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
ADD ./ /app/
