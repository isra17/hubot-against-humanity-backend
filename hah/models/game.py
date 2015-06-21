import random, os, struct
from datetime import datetime, timedelta
from hah import db, errors
from hah.models.card import Card

TURN_DURATION = timedelta(seconds=15)

class Game(db.Model):
    __tablename__ = 'games'

    id =        db.Column(db.Integer, primary_key=True)

    turn_started_at = db.Column(db.DateTime)
    turn_locked_at = db.Column(db.DateTime)
    game_stopped_at = db.Column(db.DateTime)

    players =   db.relationship(
            "Player",
            lazy='dynamic',
            foreign_keys='Player.game_id',
            backref="game",
            cascade="delete")

    active_player_id = db.Column(
            db.String,
            db.ForeignKey('players.id'),
            nullable=True)
    active_player = db.relationship(
            "Player",
            uselist=False,
            foreign_keys=[active_player_id],
            post_update=True)

    turn =	    db.Column(db.Integer, default=0)
    black_cards_picked = db.Column(db.Integer, default=0)
    white_cards_picked = db.Column(db.Integer, default=0)
    deck_size =     db.Column(db.Integer, nullable=False)
    deck_seed =     db.Column(db.Integer, nullable=False)

    def __init__(self, **kw):
        self.deck_size = Card.query.count()
        self.deck_seed = struct.unpack('i', os.urandom(4))[0]
        super().__init__(**kw)

    def players_info(self):
        return [p.serialize() for p in self.players.all()
        ]

    def active_card(self):
        if self.active_player and self.active_player.played_card:
            return self.active_player.played_card.text

    def playing_players(self):
        players = [p for p in self.players.all() \
                if p != self.active_player and p.played_card]
        random.seed(self.deck_seed + self.turn)
        random.shuffle(players)
        return players

    def played_cards(self):
        return [p.played_card.text for p in self.playing_players()]

    def lock_turn(self):
        self.turn_locked_at = datetime.utcnow()

    def turn_locked(self):
        return self.turn_locked_at is not None

    def get_active_player(self):
        return self.active_player.id if self.active_player else None

    def serialize(self, **kwargs):
        return dict({
            'id': self.id,
            'turn': self.turn,
            'active_player': self.get_active_player(),
            'active_card': self.active_card(),
            'played_cards': self.played_cards(),
            'players': self.players_info()
        }, **kwargs)

    def start_turn(self):
        for p in self.players.all():
            if p.played_card is not None and p != self.active_player:
                p.cards.remove(p.played_card)
                p.pick_cards()
            p.played_card = None

        self.rotate_active_player()
        self.turn_started_at = datetime.utcnow()
        self.turn_locked_at = None

    def check_turn_ready(self):
        players = self.players.all()
        if len([p for p in players if p.played_card]) <= 2:
            raise errors.NotEnoughPlayers()
        if datetime.utcnow() - self.turn_started_at < TURN_DURATION and \
                any(p.played_card is None for p in self.players.all()):
            raise errors.TooEarly()
        return True

    def rotate_active_player(self):
        players = self.players.all();
        if self.active_player is None:
            self.set_active_player(players[0])
        else:
            self.set_active_player(
                    players[(players.index(self.active_player)+1) % len(players)])

    def pick_white_cards(self, count):
        cards = list(range(1, self.deck_size+1))
        random.seed(self.deck_seed)
        random.shuffle(cards)
        cards = cards[self.white_cards_picked:]

        picked_cards = []
        while len(picked_cards) < count and len(cards):
            card = Card.query.get(cards.pop(0))
            if card.deleted_at is None and card.type == 'white':
                picked_cards.append(card)
            self.white_cards_picked += 1

        return picked_cards

    def draw_black_card(self):
        cards = Card.query.filter(Card.id<=self.deck_size).all()
        random.seed(self.deck_seed)
        random.shuffle(cards)
        cards = cards[self.black_cards_picked:]

        while len(cards):
            self.black_cards_picked += 1
            card = cards.pop(0)
            if card.deleted_at is None and card.type == 'black':
                return card
        return None

    def set_active_player(self, player):
        self.active_player = player
        card = self.draw_black_card()
        if card is None:
            self.end_game()
        else:
            player.played_card = card

    def end_game(self):
        self.game_stopped_at = datetime.utcnow()

    def vote(self, card_index):
        self.check_turn_ready()
        if not self.turn_locked():
            raise errors.TurnNotLocked()

        player = self.playing_players()[card_index]
        player.score += 1
        return player

