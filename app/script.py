from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
import sqlite3
import os
from config import database
from database import *

app=Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(database))

app.config.from_envvar('APP_SETTINGS', silent=True)


@app.route('/')
def home():
    db = get_db()
    cur = db.execute('select Name, Type from Event limit 5 order by Id desc')
    cur2=db.execute('select distinct City from Localization order by City')
    events = cur.fetchall()
    cities=cur2.fetchall()
    return render_template('main.html', events=events, cities=cities)


if __name__ == "__main__":
     app.run(debug=True)
