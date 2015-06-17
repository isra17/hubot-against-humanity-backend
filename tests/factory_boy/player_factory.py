import factory.alchemy
from hah.models.player import Player
from hah import db

class PlayerFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Player
        sqlalchemy_session = db.session

