FROM python:3.9-alpine
MAINTAINER Salman Barani

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /markly
WORKDIR /markly
COPY ./markly /markly

CMD ["./manage.py", "0.0.0.0:8000"]