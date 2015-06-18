import json
import unittest
import config
from datetime import datetime
from flask.ext.testing import TestCase
from hah import create_app, db
from hah.models import *
from tests.factory_boy.api_client_factory import ApiClientFactory
from tests.factory_boy.card_factory import CardFactory

def create_cards():
    for i in range(10):
        CardFactory(text='black card {}'.format(i), type='black')
    for i in range(50):
        CardFactory(text='white card {}'.format(i), type='white')

class HahTest(TestCase):
    def create_app(self):
        return create_app('config.test')

    def setUp(self):
        db.create_all()
        self.api_client = ApiClientFactory(shared_secret='\x00'*128)
        create_cards()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def auth_post(self, *args, **kwargs):
        self._add_header_auth_token(kwargs)
        return self.client.post(*args, **kwargs)

    def auth_put(self, *args, **kwargs):
        self._add_header_auth_token(kwargs)
        return self.client.put(*args, **kwargs)

    def auth_get(self, *args, **kwargs):
        self._add_header_auth_token(kwargs)
        return self.client.get(*args, **kwargs)

    def auth_delete(self, *args, **kwargs):
        self._add_header_auth_token(kwargs)
        return self.client.delete(*args, **kwargs)

    def _add_header_auth_token(self, kwargs):
        if not 'headers' in kwargs:
            kwargs['headers'] = {}

        kwargs['headers']['X-Secret-Token'] = self.api_client.shared_secret
        if 'data' in kwargs:
            kwargs['content_type'] = 'application/json'
            kwargs['data'] = json.dumps(kwargs['data'])

