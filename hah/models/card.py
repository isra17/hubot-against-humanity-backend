from datetime import datetime
from hah import db

class Card(db.Model):
    __tablename__ = 'cards'

    id =        db.Column(db.Integer, primary_key=True)

    type =      db.Column(db.Enum('white','black', name='card_type'))
    text =      db.Column(db.String)

    deleted_at =db.Column(db.DateTime)

