FROM python:3.8.2-slim-buster

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates \
      fonts-liberation \
      gconf-service \
      libappindicator1 \
      libasound2 \
      libatk-bridge2.0-0 \
      libatk1.0-0 \
      libc6 \
      libcairo2 \
      libcups2 \
      libdbus-1-3 \
      libexpat1 \
      libfontconfig1 \
      libgbm1 \
      libgcc1 \
      libgconf-2-4 \
      libgdk-pixbuf2.0-0 \
      libglib2.0-0 \
      libgtk-3-0 \
      libnspr4 \
      libnss3 \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libstdc++6 \
      libx11-6 \
      libx11-xcb1 \
      libxcb-dri3-0 \
      libxcb1 \
      libxcomposite1 \
      libxcursor1 \
      libxdamage1 \
      libxext6 \
      libxfixes3 \
      libxi6 \
      libxrandr2 \
      libxrender1 \
      libxss1 \
      libxtst6 \
      lsb-release \
      make \
      npm \
      procps \
      wget \
      xdg-utils \
 && wget -O - https://github.com/jgm/pandoc/releases/download/2.9.2.1/pandoc-2.9.2.1-linux-amd64.tar.gz| \
    tar -xz -C /usr/local/ --strip-components=1 \
 && rm -rf /usr/local/share/man/* \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /mathsnuggets

ENTRYPOINT ["make"]
