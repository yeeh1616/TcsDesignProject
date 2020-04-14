FROM python:3.8.2-alpine3.11

ENV FLASK_APP=app
ENV FLASK_ENV=development

COPY . /module_plus

WORKDIR /module_plus

COPY requirements.txt .
RUN pip install --editable .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app ./app
COPY instance ./instance
COPY project_database .

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]



