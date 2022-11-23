FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VIRTUALENVS_IN_PROJECT 1

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev

WORKDIR /code
COPY . .

RUN pip install poetry && \
    poetry install --no-dev

CMD poetry run flask --app app.server.py run
