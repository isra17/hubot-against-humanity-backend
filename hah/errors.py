from werkzeug.exceptions import HTTPException

class GameAlreadyExistError(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 1,
        'message': 'A game is already created'
    }

class PlayerAlreadyJoinedError(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 2,
        'message': 'The player already joined the game'
    }

class NoGameRunningError(HTTPException):
    code = 422
    data = {
        'status': 422,
        'code': 3,
        'message': 'No game is currently running'
    }
