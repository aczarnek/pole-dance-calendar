import sqlite3
from flask import Flask, g
from .config import database

app = Flask(__name__)
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


#sql variables to main view


queries = {
    'upcoming_events':'select Name, StartTime, Organizer, City from Event inner join Location on Location.Id = Event.LocationId order by StartTime',
    'city_option':'select distinct City from Location order by City'
}




# def insert_db(Id, Name, EventTypeId, StartTime, EndTime, Organizer, Description, LocationId):
#     conn=sqlite3.connect("app.db")
#     cur=conn.cursor()
#     cur.execute("INSERT INTO Event VALUES (?,?,?,?,?,?,?,?)",(Id, Name, EventTypeId, StartTime, EndTime, Organizer, Description, LocationId))
#     conn.commit()
#     conn.close()


# insert_db(2,'2017-11-19T12:00:00+0100', 'Pole Creativity - niezwykłe warsztaty teatralno-taneczne', 'Competition','2017-11-19T12:00:00+0100', 'Pole', 'aaa',1)
# insert_db(3,'2017-12-10T11:00:00+0100', 'Kasia Kwaśniewicz w Feniks Studio / 10 grudnia', 'Championships','2017-12-10T12:00:00+0100', 'Vertical', 'bbb', 2)
# insert_db(4,'2017-12-09T12:00:00+0100', 'FutureNet Pole Dance Championship','Championships','2017-12-09T12:00:00+0100', 'pink Puma', 'ccc', 3)

