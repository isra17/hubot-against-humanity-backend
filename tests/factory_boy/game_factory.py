import factory.alchemy
from hah.models.game import Game
from hah import db

class GameFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Game
        sqlalchemy_session = db.session

    id = factory.Sequence()

