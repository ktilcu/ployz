#!/usr/bin/python

from flask import Flask, request, g, render_template, flash, redirect, url_for, _app_ctx_stack, json
from sqlite3 import dbapi2 as sqlite3

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
    cur = g.db.execute(query, args)
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
    cur = g.db.execute('select * from ployz')
    entries = [dict(id=row[0], message=row[1], time=row[2]) for row in cur.fetchall()]
    print entries
    return render_template('showall.html', ployz=entries)


@app.route('/add', methods=['GET', 'POST'])
def add_ploy():
    if request.method == 'POST':
        db = get_db()
        post_data = request.form
        if request.headers['Content-Type'] == 'application/json':
            post_data = request.json
        print post_data
        db.execute('insert into ployz (message) values (?)', [post_data['repository']['description']])
        db.commit()
        flash('New Commit Posted')
    return redirect(url_for('viewPloyz'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
