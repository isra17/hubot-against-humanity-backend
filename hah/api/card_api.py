from flask import request
from flask.ext import restful
from hah.common.authenticate import shared_secret, ensure_game
from hah.models.card import Card
from hah import db, errors

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
        Card.query.filter_by(id=card_id).delete()
        db.session.commit()
        return {}

