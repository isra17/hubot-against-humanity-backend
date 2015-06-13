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

    channel = 	    db.Column(db.String, default='hubotagainsthumanity')
    turn =	    db.Column(db.Integer, default=0)
    cards_picked =  db.Column(db.Integer, default=0)

    def active_player_name(self):
        return self.active_player_name if self.active_player else None

    def players_names(self):
        return [p.name for p in self.players]

    def serialize(self):
        return {
            'id': self.id,
            'turn': self.turn,
            'channel': self.channel,
            'active_player': self.active_player_name(),
            'players': self.players_names()
        }
