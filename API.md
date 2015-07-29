# API

## POST /game

Create a new game

## GET /game

Get game information
```json
{
  "active_player": 123,
  "active_card": {
    "text": "The meaning of life is ______"
  },
  "game_started_at": 123123123,
  "turn_started_at": 123123123,
  "players": [{
    "id": 123,
    "score": 2,
    "has_played": false
  }, ...]
}
```

## POST /game/players

Add a player to the game.
Fields: `id`

## GET /game/players/<id>

Get player's information
```json
{
  "id": 123,
  "cards": [{
    "id": 123,
    "text": "foobar"
  }, ...]
}
```

## POST /game/players/<id>/play

Play a card
Fields: `card`: card's id

## DELETE /game/players/<id>

Leave a game
