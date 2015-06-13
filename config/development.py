import logging
import os

ENV='development'
DEBUG = True
SQLALCHEMY_ECHO = True

LOGGING_ENABLED = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/instance/hah.db'.format(os.getcwd())

