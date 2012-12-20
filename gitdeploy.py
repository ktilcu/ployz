#!/usr/bin/python

from flask import Flask, request, g, render_template, flash, redirect, url_for, _app_ctx_stack
from sqlite3 import dbapi2 as sqlite3
import time

import os
# import sqlite3

DATABASE = 'ployz.db'
DEBUG = True
SECRET_KEY = 'devkey'

app = Flask(__name__)
app.config.from_object(__name__)


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return top.sqlite_db


def query_db(query, args=(), one=False):
    try:
        cur = g.db.execute(query, args)
    except:
        init_db()
        query_db(query)
    rv = [dict((cur.description[idx][0], value)
    for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.db = get_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/')
def viewPloyz():
    entries = query_db('select * from ployz')
    print entries
    return render_template('showall.html', ployz=sorted(entries, key=lambda ploy: time.strptime(ploy['time'], '%Y-%m-%d %H:%M:%S'), reverse=True))


@app.route('/add', methods=['GET', 'POST'])
def add_ploy():
    if request.method == 'POST':
        db = get_db()
        post_data = request.form['message']
        if request.headers['Content-Type'] == 'application/json':
            post_data = request.json['repository']['description']
        print post_data
        db.execute('insert into ployz (message) values (?)', [post_data])
        db.commit()
        flash('New Commit Posted')
    return redirect(url_for('viewPloyz'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
