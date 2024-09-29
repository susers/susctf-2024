FROM golang:latest AS builder

WORKDIR /src
COPY src/ .
RUN go build

FROM debian:bookworm
WORKDIR /app
COPY --from=builder /src/waas .

COPY src/views views
COPY --chmod=0755 src/run.sh /run.sh

CMD ["/run.sh"]
