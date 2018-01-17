import sqlite3
from flask import g
from config import *

app.config.from_object(__name__)
app.config.update(database)
app.config.from_envvar('APP_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('database.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# All SQL queries
# I will delete select color in calendar_record, after update sql file and database
queries = {
    'upcoming_events': 'select Event.Id, Name, StartTime, Organizer, Description, Type, City, '
                       'AddressLine1, AddressLine2, Latitude, Longitude from Event '
                       'left join Location on Location.Id = Event.LocationId '
                       'left join EventType on EventType.Id = Event.EventTypeId '
                       'where date(StartTime)>=(?) order by StartTime limit 5;',
    'city_option': 'select distinct City from Location left join Event on Location.Id = Event.LocationId'
                   ' where date(StartTime)>=(?) order by City;',
    'calendar_record': 'select Name, StartTime, EndTime, Color from Event inner join EventType '
                       'on EventType.Id = Event.EventTypeId order by StartTime;',
    'user_events_all': 'select Event.Id, Name, StartTime, Organizer, Description, Type, City, AddressLine1, '
                       'AddressLine2, Latitude, Longitude from Event '
                       'left join EventType on EventType.Id = Event.EventTypeId left join Location '
                       'on Location.Id = Event.LocationId where EventType.Id in (?) and date(StartTime)>=(?);',
    'user_events': 'select Event.Id, Name, StartTime, Organizer, Description, Type, City, AddressLine1,'
                   ' AddressLine2, Latitude, Longitude from Event '
                   'left join EventType on EventType.Id = Event.EventTypeId '
                   'left join Location on Location.Id = Event.LocationId '
                   'where EventType.Id in (?) and date(StartTime)>=(?) and City=(?);',
    'all_events': 'select Event.Id, Name, StartTime,EndTime, Organizer, Description, Type, City, '
                       'AddressLine1, AddressLine2, Latitude, Longitude from Event '
                       'left join Location on Location.Id = Event.LocationId '
                       'left join EventType on EventType.Id = Event.EventTypeId;'
}

def insert_db(Name, EventTypeId, StartTime, EndTime, Organizer, Description, City,
              AddressLine1, AddressLine2, Latitude, Longitude):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO Location VALUES (?,?,?,?,?,?)", ('NULL', City, AddressLine1, AddressLine2,
                                                              Latitude, Longitude))
    location_id = cur.lastrowid
    cur.execute("INSERT INTO Events VALUES (?,?,?,?,?,?,?,?)",
                ('NULL', Name, EventTypeId, StartTime, EndTime, Organizer, Description, location_id))
    conn.commit()
    conn.close()
