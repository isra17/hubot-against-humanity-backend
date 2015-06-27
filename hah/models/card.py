from datetime import datetime
from hah import db

class Card(db.Model):
    __tablename__ = 'cards'

    id =        db.Column(db.Integer, primary_key=True)

    type =      db.Column(db.Enum('white','black', name='card_type'))
    text =      db.Column(db.String)

    deleted_at =db.Column(db.DateTime)

    api_client_id = db.Column(db.Integer,
                        db.ForeignKey(
                            'api_clients.id',
                            use_alter=True,
                            ondelete='CASCADE',
                            name='api_client_cards'),
                        nullable=True)

    def serialize(self):
        return {'type': self.type, 'text': self.text, 'id':self.id}
