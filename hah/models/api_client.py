from hah import db
import os

def new():
    client = ApiClient(shared_secret=os.random(32))
    return client

class ApiClient(db.Model):
    __tablename__ = 'api_clients'

    id =	    db.Column(db.Integer, primary_key=True)

    game_id =       db.Column(db.Integer, db.ForeignKey('games.id'))
    game =          db.relationship("Game", uselist=False, backref="api_client")

    shared_secret = db.Column(db.String(length=32))

