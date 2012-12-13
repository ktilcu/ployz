#!/usr/bin/python

from flask import Flask
import os

app = Flask(__name__)

from flask import request


@app.route('/', methods=['GET'])
def home():
    return 'hey dawg'


@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    return request.method

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
