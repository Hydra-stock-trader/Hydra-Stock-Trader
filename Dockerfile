FROM python:3.11-alpine

ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
COPY main.py ./
COPY .env .
COPY src ./src

RUN set -ex \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 -G appgroup --no-create-home appuser \
    && apk update \
    && apk add --no-cache procps \
    && apk upgrade \
    && pip install -r requirements.txt \
    && rm -rf /var/cache/apk/*

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]