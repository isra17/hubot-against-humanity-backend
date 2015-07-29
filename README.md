# Hubot Against Humanity

This project implements the required logic to manage and persist multiples games of Cards Against Humanity. The backend aims to be used with [this Hubot script](https://www.npmjs.com/package/hubot-hubotagainsthumanity).

## Installation

### Heroku

The project have been tested with Heroku and Python 3.4.
It must have a PostgresSql database set.

You need to generate two random secrets value (You can use `openssl rand -base64 128`). One of those secret must be shared with the Hubot script to authenticate to the API.

```
$ git clone https://github.com/isra17/hubot-against-humanity-backend.git`
$ cd hubot-against-humanity-backend
$ heroku apps:create hubot-against-humanity-backend
$ git push heroku
$ heroku config:set SECRET=$A_RANDOM_SECRET
$ heroku config:set ENV=heroku
$ heroku config:set TEST_SHARED_SECRET=$A_SECRET_SHARED_WITH_HUBOT
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku run bin/setup
$ heroku run bin/import_data
$ heroku ps:scale web=1
```

And the backend should be up and running!

