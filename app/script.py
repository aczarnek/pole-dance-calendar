from flask import render_template
from .database import *


@app.route('/')
def home():
    db = get_db()
    cur = db.execute('select Name, Type from Event order by Name desc')
    cur2=db.execute('select distinct Description from Event order by Description')
    events = cur.fetchall()
    cities=cur2.fetchall()
    return render_template('main.html', events=events, cities=cities)


if __name__ == "__main__":
     app.run(debug=True)
