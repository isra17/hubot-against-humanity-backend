from hah import db

PlayerCard = Table('player_cards', db.Model.metadata,
    db.Column('player_id', Integer, ForeignKey('players.id')),
    db.Column('card_id', Integer, ForeignKey('cards.id'))
)

class Player(db.Model):
    __tablename__ = 'players'

    id =	    db.Column(db.Integer, primary_key=True)

    game_id =       db.Column(Integer, ForeignKey('games.id'))
    cards =         db.relationship("Card", secondary=PlayerCard)

    played_card_id =db.Column(db.Integer, ForeignKey('cards.id'), nullable=True)
    played_card =   db.relationship("Card", uselist=False)

    name = 	    db.Column(db.String)
    score =	    db.Column(db.Integer)

