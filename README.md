surl
====

Url Shortener made with python and Flask and MongoDB.

Just run it as any other Flask app.

ivanb@local:~/workspace/surl$ python shortener.py

To test it, execute this:
curl -d "link=https://github.com/ipedrazas" http://localhost:5001

It will return a json doc like this one:

{
  "url": "http://127.0.0.1:5001/GTR"
}

Nothing fancy, as I said.
