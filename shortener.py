from flask import Flask, request, redirect, abort, jsonify
app = Flask(__name__)

from random import  sample
from string import digits, ascii_letters
from pymongo import Connection
from datetime import datetime
import os


try:
    URL = os.environ['URL']
    DB_URL = os.environ['DB_URL']
    NUM_CHARS = os.environ['NUM_CHARS']
except:
    URL = 'http://localhost:5000/'
    DB_URL = 'mongodb://localhost:27017'
    NUM_CHARS = 3


conn = Connection(DB_URL)
db = conn['shurls']
objects = db['urls']
num = int(NUM_CHARS)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Url Shortener made with MongoDB, Flask and python, of course!'


@app.route('/stats/<url_id>', methods=['GET'])
def stats(url_id=None):
    if url_id:
        url = objects.find_one({'url_id': url_id})
        if url:
            url['id'] = str(url['_id'])
            url['added'] = date_to_str(url['added'])
            del url['_id']
            return jsonify({'stats': url})


@app.route('/<url_id>', methods=['GET'])
def get(url_id=None):
    if url_id:
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
        return jsonify({'url': URL + url['url_id']})
    else:
        return jsonify({'url': URL + short_id(link)})


def date_to_str(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%d-%m-%Y- %H:%M:%S')


if __name__ == '__main__':
     # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
