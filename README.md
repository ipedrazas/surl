shurl
====

Url Shortener made with python and Flask and MongoDB.

It's basically a very simple REST service with 3 methods:

::

    GET: /<link_id> -> returns the original url
    POST: / link=url -> returns the shortened url
    GET: /stats/<link_id> -> returns the stats of the url

It comes ready to run under a virtualenv, so, after clonning the repo, activate virtualenv, install dependencies and run it (python shortener.py will do)

There are only 2 dependencies:
- [Flask](http://flask.pocoo.org/)
- [pymongo](http://api.mongodb.org/python/current/)

install & config Virtualenv
---------------------------
    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt
    python shortener


To test it, execute this:
::

    curl -d "link=https://github.com/ipedrazas" http://localhost:5000

    It will return a json doc like this one:
        {
          "url": "http://127.0.0.1:5000/G4Tr"
        }

    This is an example of the Stats call

        {
          "stats": {
            "hits": 3,
            "url_id": "bEk",
            "added": "23-08-2012- 13:44:23",
            "link": "http://ducksboard.com/pricing/",
            "saved": 8,
            "id": "503633b72ba78b2f3f50527a"
          }
        }

Nothing fancy, as I said.

Running as an Heroku Instance
-----------------------------

In case you want to run it in Heroku, set the variables first:

heroku config:add URL=http://myapp_name.herokuapp.com/ DB_URL=mongodb://my_user:my_password@my_mongodb_server:my_mongodb_port NUM_CHARS=4

You have to install a mongodb instance, since this app doesn't include the database you could use [MongoLab](https://mongolab.com) where the first 240Mb are free.
