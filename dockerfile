FROM adoptopenjdk/openjdk11-openj9:jdk-11.0.13_8_openj9-0.29.0-debian
RUN mkdir /app
RUN cp -R /opt/java/openjdk /app

FROM python:3.8-slim-buster

RUN apt-get update \
  && apt-get install -y --no-install-recommends procps gdb git curl inotify-tools \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
RUN /root/.local/bin/poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml /app/
WORKDIR /app/
RUN /root/.local/bin/poetry install --no-interaction --no-root

COPY src /app/src
RUN /root/.local/bin/poetry install

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"

#run on jenkens