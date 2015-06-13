from hah import db

PlayerCard = db.Table('player_cards', db.Model.metadata,
    db.Column('player_id', db.Integer, db.ForeignKey('players.id')),
    db.Column('card_id', db.Integer, db.ForeignKey('cards.id'))
)

class Player(db.Model):
    __tablename__ = 'players'

    id =	    db.Column(db.Integer, primary_key=True)
    order_id =      db.Column(db.Integer, db.Sequence('order_seq'))

    game_id =       db.Column(db.Integer,
                        db.ForeignKey(
                            'games.id',
                            use_alter=True,
                            name='player_game'))
    cards =         db.relationship("Card", secondary=PlayerCard)

    played_card_id =db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=True)
    played_card =   db.relationship("Card", uselist=False)

    score =	    db.Column(db.Integer, default=0)

    def serialize(self):
        return {
            'id': self.id,
            'cards': [],
            'played_card': None,
            'score': self.score
        }
