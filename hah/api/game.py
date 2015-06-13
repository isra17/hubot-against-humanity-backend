from flask.ext import restful
from hah.common.authenticate import shared_secret

class Game(restful.Resource):
    method_decorators=[shared_secret]

    def get(self):
        return {
            'id': 1,
            'player': [],
            'turn': 0
        }

    def post(self):
        return {
            'id': 1,
            'player': [],
            'turn': 0
        }

