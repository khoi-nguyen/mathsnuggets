FROM python:3.8.2-slim-buster

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      make \
      npm \
      wget \
 && wget -O - https://github.com/jgm/pandoc/releases/download/2.9.2.1/pandoc-2.9.2.1-linux-amd64.tar.gz| \
    tar -xz -C /usr/local/ --strip-components=1 \
 && apt-get -y remove wget \
 && rm -rf /usr/local/share/man/* \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /mathsnuggets

ENTRYPOINT ["make"]
