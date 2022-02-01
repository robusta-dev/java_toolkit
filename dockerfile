FROM adoptopenjdk/openjdk11-openj9:jdk-11.0.13_8_openj9-0.29.0-debian

RUN apt-get update \
  && apt-get install -y --no-install-recommends procps gdb git curl inotify-tools \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app/
COPY ../../src /app/src
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"

#run on jenkens