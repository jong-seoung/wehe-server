FROM python:3.9.6

RUN apt-get update && apt-get install -y nano vim

WORKDIR /weheproject

ENV DJANGO_SETTINGS_MODULE=weheproject.settings.jongs-dev
ENV PYTHONUNBUFFERED 1

COPY Pipfile Pipfile.lock ./

RUN pip install -U pipenv
RUN pipenv install --system --dev