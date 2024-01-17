FROM python:3.11-slim

RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y build-essential curl ffmpeg git libpq-dev libssl-dev locales tini unzip

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY api /api

COPY tests /tests

ENTRYPOINT ["tini", "--"]

CMD ["sanic", "api.app", "--host=0.0.0.0", "--port=5678"]
