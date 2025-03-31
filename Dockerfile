FROM python:3.12-slim-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYSETUP_PATH="/opt/app" \
    UV_VERSION="0.5.29"

WORKDIR $PYSETUP_PATH

RUN pip install --no-cache-dir uv==$UV_VERSION

COPY ./pyproject.toml ./README.md ./
COPY ./src ./src

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install -e .

FROM python:3.12-slim-bookworm

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /opt/app

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /opt/app/src ./src

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
