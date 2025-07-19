FROM python:3.8-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget build-essential git && \
    rm -rf /var/lib/apt/lists/* && \
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

WORKDIR /app

COPY . .

ARG GH_PAT
ARG PORT

ENV GH_PAT=${GH_PAT}
ENV PORT=${PORT}

RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /app/venv/bin/pip install --no-cache-dir TA-Lib==0.4.37 && \
    /app/venv/bin/pip install --no-cache-dir git+https://${GH_PAT}:x-oauth-basic@github.com/Backtesting-IO/backtesting-io-manager.git@main

FROM python:3.8-slim

COPY --from=builder /usr/lib/libta_lib.* /usr/lib/
COPY --from=builder /usr/include/ta-lib/ /usr/include/ta-lib/
COPY --from=builder /app/venv /app/venv
COPY --from=builder /app/main.py /app/main.py
COPY --from=builder /app/indicator_service /app/indicator_service

WORKDIR /app

COPY main.py /app

COPY . /app/

EXPOSE $PORT

ENTRYPOINT ["/app/venv/bin/python","/app/main.py"]