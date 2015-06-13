from datetime import datetime
from hah import db

class Cards(db.Model):
    __tablename__ = 'cards'

    id =        db.Column(db.Integer, primary_key=True)

    type =      db.Column(db.Enum('white','black'))
    text =      db.Column(db.String)

