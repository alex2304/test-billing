FROM python:3.9-alpine

ENV PYTHONPATH=${PYTHONPATH}:/app

WORKDIR /app

ADD ./requirements.txt .
RUN apk update && apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir -r requirements.txt && \
    apk --purge del .build-deps

RUN apk add curl

COPY ./src .

EXPOSE 8000
