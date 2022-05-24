FROM docker.io/tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

ENV PYTHONUNBUFFERED=TRUE
ENV PORT=8080

EXPOSE 8080

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev curl
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o rustup.sh
RUN chmod u+x ./rustup.sh && ./rustup.sh -y
RUN cp ~/.cargo/bin/rustc /bin
RUN cp ~/.cargo/bin/cargo /bin
RUN pip install cryptography
COPY *.py /app

