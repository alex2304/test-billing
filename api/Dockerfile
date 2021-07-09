FROM python:3.9-alpine

ENV PYTHONPATH=${PYTHONPATH}:/app

WORKDIR /app

ADD ./requirements.txt .
RUN apk update && apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir -r requirements.txt && \
    apk --purge del .build-deps

COPY ./src .

COPY pytest.ini .
RUN pytest
RUN rm test_routes.py pytest.ini requirements.txt
