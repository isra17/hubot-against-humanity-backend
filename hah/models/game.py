from datetime import datetime
from hah import db
from hah.models.card import Card

class Game(db.Model):
    __tablename__ = 'games'

    id =        db.Column(db.Integer, primary_key=True)

    players =   db.relationship(
            "Player",
            order_by='Player.id',
            foreign_keys='Player.game_id',
            backref="game")

    active_player_id = db.Column(
            db.Integer,
            db.ForeignKey('players.id'),
            nullable=True)
    active_player = db.relationship(
            "Player",
            uselist=False,
            foreign_keys=[active_player_id])

    turn =	    db.Column(db.Integer, default=0)
    cards_picked =  db.Column(db.Integer, default=0)

    def players_ids(self):
        return [p.id for p in self.players]

    def serialize(self):
        return {
            'id': self.id,
            'turn': self.turn,
            'active_player': self.active_player,
            'players': self.players_ids()
        }

    def pick_cards(self, count):
        return [Card()]

