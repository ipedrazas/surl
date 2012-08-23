# Copyright 2012 Ivan Pedrazas
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from flask import Flask, request, redirect, abort, jsonify
app = Flask(__name__)

from random import sample
from string import digits, ascii_letters
from pymongo import Connection
from datetime import datetime
import os

#
# There are 3 parameters to config this app:
# - DB_URL: url to the mongodb database. Default is 'mongodb://localhost:27017'
# - URL: url used as base of the redirection. If you were running bit.ly this param would be "http://bit.ly"
# - NUM_CHARS: length of the id for the shortened URLs. 3 will generate ids like '2dT' or 'oi5'. 4 would be 'ty56', etc...
#               Yes, you can start with a low number and increase it as needed (if needed. 3 chars > 175K Urls)
#
# If you use heroku set these variables using
#   heroku config:add URL=http://myurl.com/ DB_URL=mongodb://my_user:my_password@my_mongodb_server:my_mongodb_port NUM_CHARS=4
# otherwise, if will fallback to the vars in the except block
#
try:
    URL = os.environ['URL']
    DB_URL = os.environ['DB_URL']
    NUM_CHARS = os.environ['NUM_CHARS']
    SECRET = os.environ['SECRET']
except:
    URL = 'http://localhost:5000/'
    DB_URL = 'mongodb://localhost:27017'
    NUM_CHARS = 3
    SECRET = 'secret'


conn = Connection(DB_URL)
db = conn['shurls']  # shurls is the database where the urls will be stored
objects = db['urls']  # urls is the name of the collection. From mongo shell, you would do db.urls.find()
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
    abort(404)


@app.route('/<url_id>', methods=['GET'])
def get(url_id=None):
    if url_id:
        url = objects.find_one({'url_id': url_id})
        if url:
            objects.update({'_id': url['_id']}, {'$inc': {'hits': 1}})
            return redirect(url['link'], 301)
    abort(404)


def short_id(link):
        url_id = "".join(sample(digits + ascii_letters, num))
        objects.insert({'url_id': url_id, 'link': link, 'hits': 0, 'saved': 0, 'added': datetime.utcnow()})
        return url_id


@app.route('/', methods=['POST'])
def add():
    link = request.form['link']
    auth_token = request.form['key']
    if auth_token != SECRET:
        abort(401)
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
