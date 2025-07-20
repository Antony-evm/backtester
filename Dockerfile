FROM python:3.8-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      wget build-essential git && \
    rm -rf /var/lib/apt/lists/*

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && make install && \
    cd .. && rm -rf ta-lib*

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /app/venv/bin/pip install --no-cache-dir TA-Lib==0.4.37

FROM python:3.8-slim
COPY --from=builder /usr/lib/libta_lib.* /usr/lib/
COPY --from=builder /usr/include/ta-lib/ /usr/include/ta-lib/
COPY --from=builder /app/venv /app/venv

WORKDIR /app

COPY backtester/ ./backtester/

ARG PORT
ENV PORT=${PORT}
EXPOSE ${PORT}
ENTRYPOINT ["/app/venv/bin/python","/app/main.py"]