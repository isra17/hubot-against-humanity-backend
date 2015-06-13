import factory.alchemy
from hah.models.api_client import ApiClient
from hah import db

class ApiClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ApiClient
        sqlalchemy_session = db.session

