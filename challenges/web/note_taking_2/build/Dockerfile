FROM node:latest

RUN apt update && \
    apt install -y curl gnupg2

RUN apt-get update && \
    apt-get install chromium -y --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
ENV NODE_ENV=production
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

WORKDIR /app

RUN mkdir /app/public

COPY src/package*.json .

RUN npm install

COPY src/ .

RUN useradd -ms /bin/bash user
RUN chown -R user:user /app/public
RUN chmod -R +rx /app
USER user

CMD ["node", "app.js"]

