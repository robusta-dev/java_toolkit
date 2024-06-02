FROM python:3.12-slim as builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app
RUN apt-get update \
  && apt-get install -y gcc

RUN python -m venv /app/venv
RUN pip install poetry==1.6.1
COPY poetry.lock pyproject.toml additional_bash_commands.sh /app/

RUN poetry install --no-interaction --no-root

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

COPY poetry.lock pyproject.toml additional_bash_commands.sh /app/
RUN cat additional_bash_commands.sh >> ~/.bashrc
COPY src/jattach  /app/openjdk/jattach

COPY --from=builder /app/venv /venv

ENV PYTHONPATH=$PYTHONPATH:.

# -u disables stdout buffering https://stackoverflow.com/questions/107705/disable-output-buffering
# TODO: use -u in developer builds only
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"

