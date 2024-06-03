FROM python:3.12-slim as builder

ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

RUN apt-get update \
  && apt-get install -y gcc
RUN pip install poetry==1.6.1

COPY poetry.lock pyproject.toml /app/

COPY src /app/src

RUN python -m venv /app/venv && \
    . /app/venv/bin/activate && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

FROM python:3.12-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH=$PYTHONPATH:.:/app
COPY src/jattach  /app/openjdk/jattach
COPY --from=builder /app/venv /venv

COPY src /app/src

RUN echo -e '#!/bin/bash\npython /app/src/java_toolkit/main.py $@' > /usr/bin/java-toolkit && \
    chmod +x /usr/bin/java-toolkit

# -u disables stdout buffering https://stackoverflow.com/questions/107705/disable-output-buffering
# TODO: use -u in developer builds only
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"

