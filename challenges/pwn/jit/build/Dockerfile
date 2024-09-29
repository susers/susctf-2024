FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends xinetd python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf
WORKDIR /home/ctf
COPY --chown=ctf:ctf --chmod=0700 src/ .
COPY --chown=root:root --chmod=0400 ctf.xinetd /etc/xinetd.d/ctf

CMD [ "/home/ctf/run.sh" ]

EXPOSE 9999
