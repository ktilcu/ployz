#!/usr/bin/python

from flask import Flask
app = Flask(__name__)

from flask import request


@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    print request.form
    return request.method

if __name__ == '__main__':
    app.run()
