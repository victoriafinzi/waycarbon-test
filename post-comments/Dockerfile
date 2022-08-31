FROM python:alpine

RUN apk add --no-cache openssl-dev musl-dev libffi-dev libmagic gcc g++ cargo
RUN apk add --no-cache python3-dev libjpeg-turbo-dev zlib-dev
RUN apk add --no-cache git openssh
RUN pip install poetry

RUN mkdir /app
WORKDIR /app

ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

EXPOSE 5000
CMD poetry install \
    && poetry run python -m scripts.populate_db \
    && poetry run flask run -h 0.0.0.0 -p 5000
