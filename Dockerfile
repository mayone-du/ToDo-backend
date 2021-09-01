FROM python:3.9.6-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /workdir

COPY requirements.txt /workdir/

RUN \
  # pip自体のアップグレード
  pip install --upgrade pip && \
  # requirements.txtからパッケージをインストール
  pip install -r requirements.txt
