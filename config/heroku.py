from os import environ

ENV='heroku'
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
SECRET = environ.get('SECRET')
if 'ROLLBAR_ACCESS_TOKEN' in environ:
    ROLLBAR_ACCESS_TOKEN = environ.get('ROLLBAR_ACCESS_TOKEN')

