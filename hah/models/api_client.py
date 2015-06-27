from hah import db
import os

def new():
    import base64
    client = ApiClient(shared_secret=base64.b64encode(os.urandom(64)))
    return client

class ApiClient(db.Model):
    __tablename__ = 'api_clients'

    id =	    db.Column(db.Integer, primary_key=True)

    game_id =       db.Column(db.Integer, db.ForeignKey('games.id', ondelete="SET NULL"), nullable=True)
    game =          db.relationship("Game", uselist=False)

    shared_secret = db.Column(db.String(length=88))

    cards =   db.relationship(
            "Card",
            lazy='dynamic',
            foreign_keys='Card.api_client_id',
            backref="api_client",
            cascade="delete",
            order_by='Card.id')

    def cards_info(self):
        return [c.serialize() for c in self.cards.all()]

