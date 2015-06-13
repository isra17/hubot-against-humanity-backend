from datetime import datetime
from hah import db

class Game(db.Model):
    __tablename__ = 'games'

    id =        db.Column(db.Integer, primary_key=True)

    players =   db.relationship(
            "Player",
            order_by='Player.id',
            foreign_keys='Player.game_id')

    active_player_id = db.Column(
            db.Integer,
            db.ForeignKey('players.id'),
            nullable=True)
    active_player = db.relationship(
            "Player",
            uselist=False,
            foreign_keys=[active_player_id])

    channel = 	    db.Column(db.String)
    turn =	    db.Column(db.Integer)
    cards_picked =  db.Column(db.Integer)

