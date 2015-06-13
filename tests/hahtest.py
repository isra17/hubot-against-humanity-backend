import unittest
import config
from datetime import datetime
from flask.ext.testing import TestCase
from hah import create_app, db
from hah.models import *

class HahTest(TestCase):
    def create_app(self):
        return create_app('config.test')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def auth_post(self, *args, **kwargs):
        self._add_header_auth_token(kwargs)
        return self.client.post(*args, **kwargs)

    def auth_get(self, *args, **kwargs):
        self._add_header_auth_token(kwargs)
        return self.client.get(*args, **kwargs)

    def _add_header_auth_token(self, kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['X-Secret-Token'] = config.test.SHARED_SECRET

