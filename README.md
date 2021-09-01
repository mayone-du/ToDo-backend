# 概要

api 内はアプリ用のサンプル
それ以外はプロジェクト用のサンプル

## セットアップ

クローン後、下記コマンドを順に実行

- pipenv shell
- pipenv install --dev
<!-- - pip freeze > requirements.txt -->
- docker-compose up --build
- docker-compose exec app bash
- django-admin startproject project .
  .env に SECRET_KEY などを色々設定
- python manage.py startapp api
  api という名前のアプリを作ったら、project/settings.py の api 部分のコメントを解除し、api で models を定義
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver 0.0.0.0:8000

### /.env

SECRET_KEY
DEBUG

DB_NAME
DB_USER
DB_HOST

CLOUDINARY_API_SECRET

EMAIL_HOST
EMAIL_HOST_USER
EMAIL_HOST_PASSWOR
EMAIL_PORT

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

## デプロイ（Heroku）

- heroku config:push
  ...
- git push heroku master
- heroku run python3 manage.py migrate
- heroku run python3 manage.py createsuperuser
