from hah import db
from .card import Card

PlayerCard = db.Table('player_cards', db.Model.metadata,
    db.Column('player_id', db.String, db.ForeignKey('players.id', ondelete='CASCADE')),
    db.Column('card_id', db.Integer, db.ForeignKey('cards.id'))
)

MAX_CARD_COUNT = 10

class Player(db.Model):
    __tablename__ = 'players'

    id =	    db.Column(db.String, primary_key=True)
    order_id =      db.Column(db.Integer, db.Sequence('order_seq'))

    left_at =       db.Column(db.DateTime)

    game_id =       db.Column(db.Integer,
                        db.ForeignKey(
                            'games.id',
                            use_alter=True,
                            ondelete='CASCADE',
                            name='player_game'))
    cards =         db.relationship("Card", secondary=PlayerCard, order_by=Card.id, cascade="delete")

    played_card_id =db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=True)
    played_card =   db.relationship("Card", uselist=False)

    score =	    db.Column(db.Integer, default=0)

    def cards_text(self):
        return [c.text for c in self.cards]

    def played_card_info(self):
        if self.played_card is not None and self.played_card in self.cards:
            return {
                    'id': self.cards.index(self.played_card),
                    'text': self.played_card.text
            }

    def serialize(self):
        return {
            'id': self.id,
            'cards': self.cards_text(),
            'played_card': self.played_card_info(),
            'score': self.score
        }

    def pick_cards(self):
        cards = self.game.pick_white_cards(MAX_CARD_COUNT - len(self.cards))
        for card in cards:
            self.cards.append(card)

