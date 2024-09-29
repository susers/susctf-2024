FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y php-cli sudo && \
    pip3 install flask && \
    mkdir /sandbox && chown www-data /sandbox

COPY src /app
COPY --chmod=0755 run.sh /run.sh

RUN chmod -R 755 /app

WORKDIR /app

CMD ["/run.sh"]
