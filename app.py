#!/usr/bin/python

from flask import Flask
app = Flask(__name__)

from flask import request


@app.route('/', methods=['GET'])
def home():
    return 'hey dawg'


@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    return request.method

if __name__ == '__main__':
    app.run()
