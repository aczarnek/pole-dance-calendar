from flask import render_template, request, json
from .database import *
from datetime import datetime as dt
from flask_googlemaps import GoogleMaps


now = dt.now()
# You can easily get a key from https://developers.google.com/maps/documentation/javascript/get-api-key
GoogleMaps(app, key="XXX")

@app.route('/')
def home():
    db = get_db()
    cur = db.execute(queries['upcoming_events'], (now,))
    cur2 = db.execute(queries['city_option'], (now,))
    upcoming_events = cur.fetchall()
    cities = cur2.fetchall()
    email = 'poledancecalendar@gmail.com'

    return render_template('main.html', upcoming_events=upcoming_events, cities=cities, email=email)


@app.route('/data')
def return_data():

    with open("../records_json.json", "r") as input_data:
        return input_data.read()


@app.route('/events', methods=['POST'])
def events():
    # variables from form
    event_type = request.values.getlist('eventType')
    city = request.form['city2']

    # check if user chose type of the event and city
    if len(event_type) < 1 or city == 'City':
        if len(event_type) < 1:
            return json.dumps({'type_error': 'Select type of events'})

        else:
            return json.dumps({'city_error': 'Select city'})

    # if user chose type and city database connection will be created
    else:
        db = get_db()
        all_events = []
        user_events_type = []

        for i in event_type:
            # if user chose all cities query will display events from the whole Poland
            if city == 'All cities':
                cur = db.execute(queries['user_events_all'], (i, now))

            else:
                cur = db.execute(queries['user_events'], (i, now, str(city)))

            user_events = cur.fetchall()

            if len(user_events) > 0:
                user_events_type.append(user_events)

        all_user_events = [i for sublist in user_events_type for i in sublist]

        # prepare dict with events
        user_events_dict = []
        for row in all_user_events:
            event_dict = {
                'Id': row['Id'],
                'Name': row['Name'],
                'Start': row['StartTime'],
                'City': row['City'],
                'Organizer': row['Organizer'],
                'Type': row['Type'],
                'Description': row['Description'],
                'AddressLine1': row['AddressLine1'],
                'AddressLine2': row['AddressLine2'],
                'Latitude': row['Latitude'],
                'Longitude': row['Longitude'],
            }

            user_events_dict.append(event_dict)

        all_events.append(user_events_dict)

        # if database don't contain events with selected options it returns empty_error
        if len(all_events[0]) < 1:
            return json.dumps({'empty_error': 'No events'})

        #return json with user events
        return json.dumps(all_events)



if __name__ == "__main__":
    app.run(debug=True)
