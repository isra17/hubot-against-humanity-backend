import random, os, struct
from datetime import datetime
from hah import db
from hah.models.card import Card

class Game(db.Model):
    __tablename__ = 'games'

    id =        db.Column(db.Integer, primary_key=True)

    players =   db.relationship(
            "Player",
            lazy='dynamic',
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
    deck_size =     db.Column(db.Integer, nullable=False)
    deck_seed =     db.Column(db.Integer, nullable=False)

    def __init__(self, **kw):
        self.deck_size = Card.query.count()
        self.deck_seed = struct.unpack('I', os.urandom(4))[0]
        super().__init__(**kw)

    def players_ids(self):
        return [p.id for p in self.players.all()]

    def serialize(self):
        return {
            'id': self.id,
            'turn': self.turn,
            'active_player': self.active_player,
            'players': self.players_ids()
        }

    def pick_white_cards(self, count):
        cards = list(range(1, self.deck_size+1))
        random.seed(self.deck_seed)
        random.shuffle(cards)
        cards = cards[self.cards_picked:]

        picked_cards = []
        while len(picked_cards) < count and len(cards):
            card = Card.query.get(cards.pop(0))
            if card.deleted_at is None and card.type == 'white':
                picked_cards.append(card)
            self.cards_picked += 1

        return picked_cards

