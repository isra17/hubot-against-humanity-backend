from flask import request
from flask.ext import restful
from hah.common.authenticate import shared_secret, ensure_game
from hah.models.card import Card
from hah import db, errors
from datetime import datetime

class CardsApi(restful.Resource):
    method_decorators=[shared_secret]

    def get(self, api_client):
        return api_client.cards_info()

    def post(self, api_client):
        card_type = request.json['type']
        text = request.json['text']
        card = Card(type=card_type, text=text)
        api_client.cards.append(card)
        db.session.add(card)
        db.session.commit()
        return card.serialize()

class CardApi(restful.Resource):
    method_decorators=[shared_secret]
    def delete(self, api_client, card_id):
        card = Card.query.filter_by(api_client=api_client, id=card_id).first()
        card.deleted_at = datetime.utcnow()
        db.session.commit()
        return {}

