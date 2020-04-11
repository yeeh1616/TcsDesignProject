FROM utwentefmt/tool-server:v1.0.1
#FROM python:3.6-alpine
#FROM python:3.7.2-stretch

WORKDIR /app

ADD . /app

RUN set -xe \
    && apt-get update \
    && apt-get install python-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#CMD ["uwsgi", "app.ini"]
