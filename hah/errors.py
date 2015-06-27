from werkzeug.exceptions import HTTPException

class GameAlreadyExistError(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 1,
        'message': 'A game is already running'
    }

class PlayerAlreadyJoinedError(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 2,
        'message': 'You already joined the game'
    }

class NoGameRunningError(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 3,
        'message': 'No game is currently running'
    }

class ParametersMissing(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 4,
        'message': 'Parameters missing'
    }

    def __init__(self, param):
        super().__init__()
        self.data['message'] = 'Parameters "{}" missing'.format(param)

class InvalidCard(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 5,
        'message': 'This card is invalid'
    }

class PlayerCantPlay(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 6,
        'message': 'You cannot play a card'
    }

class TooEarly(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 7,
        'message': 'You cannot vote yet'
    }

class NotEnoughPlayers(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 8,
        'message': 'There need to be at least 2 players that played a card'
    }

class TurnNotLocked(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 9,
        'message': 'You need to wait a bit more or that all player have played'
    }

class TurnLocked(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 10,
        'message': 'You cannot play a card while a player is voting'
    }

class PlayerCantVote(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 11,
        'message': 'You are not the voting player'
    }
