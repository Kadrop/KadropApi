FROM python:latest

MAINTAINER Raphael Courivaud "r.courivaud@gmail.com"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["gunicorn",  "--bind",  "0.0.0.0:80", "wsgi"]