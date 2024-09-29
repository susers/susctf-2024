FROM ubuntu:24.04 AS builder

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y build-essential libmicrohttpd12t64 libmicrohttpd-dev

COPY incbin.h index.html server.c .

RUN gcc -o server server.c -lmicrohttpd

FROM ubuntu:24.04

WORKDIR /app

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y libmicrohttpd12t64 w3m w3m-img xvfb xterm

COPY --from=builder server .

CMD ["/app/server", "8080"]
