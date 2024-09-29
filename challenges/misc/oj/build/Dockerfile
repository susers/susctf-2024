FROM python:3.12-alpine

RUN pip3 --no-cache-dir install fastapi "uvicorn[standard]" PyNaCl && apk add g++ libseccomp-dev linux-headers

RUN adduser -D -h /app app
WORKDIR /app
COPY --chown=app:app --chmod=0700 app/ .

CMD [ "/app/run.sh" ]
