import factory.alchemy
from hah.models.card import Card
from hah import db

class CardFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Card
        sqlalchemy_session = db.session

