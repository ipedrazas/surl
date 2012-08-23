from flask import Flask, request, redirect, abort, jsonify
app = Flask(__name__)

from random import  sample
from string import digits, ascii_letters
from pymongo import Connection
from datetime import datetime

conn = Connection()
db = conn['shurls']
objects = db['urls']
num = 3

SERVER_NAME = '127.0.0.1'
SERVER_PORT = 5001
BASE = 'http://%s:%s' % (SERVER_NAME, str(SERVER_PORT))


@app.route('/', methods=['GET'])
def hello_world():
    return 'Url Shortener made with MongoDB, Flask and python, of course!'


@app.route('/<url_id>', methods=['GET'])
def get(url_id=None):
    url = objects.find_one({'url_id': url_id})
    if url:
        objects.update({'_id': url['_id']}, {'$inc': {'hits': 1}})
        return redirect(url['link'], 301)
    return abort(404)


def short_id(link):
        url_id = "".join(sample(digits + ascii_letters, num))
        objects.insert({'url_id': url_id, 'link': link, 'hits': 0, 'saved': 0, 'added': datetime.utcnow()})
        return url_id


@app.route('/', methods=['POST'])
def add():
    link = request.form['link']
    url = objects.find_one({'link': link})
    if url:
        objects.update({'_id': url['_id']}, {'$inc': {'saved': 1}})
        return jsonify({'url': BASE + '/' + url['url_id']})
    else:
        return jsonify({'url': BASE + '/' + short_id(link)})

if __name__ == '__main__':
    app.run(SERVER_NAME, SERVER_PORT, debug=True)

