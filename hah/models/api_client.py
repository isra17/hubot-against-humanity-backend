from hah import db
import os

def new():
    import base64
    client = ApiClient(shared_secret=base64.b64decode(os.urandom(64)))
    return client

class ApiClient(db.Model):
    __tablename__ = 'api_clients'

    id =	    db.Column(db.Integer, primary_key=True)

    game_id =       db.Column(db.Integer, db.ForeignKey('games.id'), nullable=True)
    game =          db.relationship("Game", uselist=False)

    shared_secret = db.Column(db.String(length=88))

