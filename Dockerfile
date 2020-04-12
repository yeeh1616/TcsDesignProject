FROM python:3.6-alpine

RUN adduser -D module_plus

WORKDIR /home/module_plus

#ADD . /app

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY instance instance
COPY run.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

RUN chown -R module_plus:module_plus ./
USER module_plus

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]