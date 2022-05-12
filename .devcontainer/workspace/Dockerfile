# FROM python:3.7.3-slim
FROM python:3.8-alpine

# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#     apt-utils \
#     gcc \
#     build-essential \
#     && pip install --no-cache-dir \
#     autopep8 \
#     flake8 \
#     pytest \
#     && apt-get autoremove -y \
#     && apt-get clean -y \
#     && rm -rf /var/lib/apt/lists/*

RUN apk update \
    && apk add musl-dev gcc make g++ file alpine-sdk \
    && pip install --upgrade pip \
    && pip install --no-cache-dir \
    autopep8 \
    flake8 \
    pytest

RUN apk add --no-cache sudo

ARG USERNAME
ARG UID
ARG GID

RUN apk add --no-cache shadow \
    && groupadd --gid $GID $USERNAME \
    && useradd --uid $UID --gid $GID -m $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apk del shadow

USER $USERNAME


