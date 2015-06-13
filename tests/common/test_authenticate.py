from flask_restful import Resource
from hah import db
from tests.hahtest import HahTest
from unittest import mock
import json

class AuthenticateTest(HahTest):
    def test_invalid_secret(self):
        rv = self.client.post('/game',
                headers={'X-Secret-Token': 'foobar'})
        self.assert_401(rv)
