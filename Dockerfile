FROM python:3.7-alpine
MAINTAINER Shaka Kanenobu

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .temp-build-dep \ 
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .temp-build-dep


RUN mkdir /app
WORKDIR /app
COPY ./app /app


RUN adduser -D user
USER user

COPY wait-for-it.sh wait_for_it.sh
RUN chmod + x wait-for-it.sh

CMD ["./wait-for-it.sh", "db:5432", "--", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]