from flask import render_template
from .database import *


@app.route('/')
def home():
    db = get_db()
    cur = db.execute(queries['upcoming_events'])
    cur2 = db.execute(queries['city_option'])
    events = cur.fetchall()
    cities = cur2.fetchall()
    email='poledancecalendar@gmail.com'
    return render_template('main.html', events=events, cities=cities, email=email)

@app.route('/data')
def return_data():
    # start_date = request.args.get('start', '')
    # end_date = request.args.get('end', '')

    with open("events.json", "r") as input_data:
        return input_data.read()

if __name__ == "__main__":
    app.run(debug=True)
