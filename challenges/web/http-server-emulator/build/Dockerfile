FROM denoland/deno:1.46.3 AS builder

WORKDIR /src
COPY src/ .
RUN deno task rel

FROM denoland/deno:1.46.3
WORKDIR /app
COPY --from=builder /src/hse .

COPY src/index.html .

COPY src/requests requests

CMD ["/app/hse"]
