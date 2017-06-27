import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
from flask import Flask, request, json

app = Flask(__name__)

### app config start

app.config.from_object(__name__) # load config from this file , carcampr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'data/db.sqlite'),
    SECRET_KEY='93WQPOOX8VO49uf5Sy0xIMgwSh7KmaPWR2tr',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('CARCAMPR_SETTINGS', silent=True)

### app config end

### db helper functions start

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the current application context. """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

### db helper functions stop

def save_new_location():
    return 'received location post request. Saving Json: %s' % request.get_json()

def show_all_locations():
    return 'All of the locations!'

@app.route('/')
def hello_world():
    return 'Hello! This is the placeholder index page!'

@app.route('/locations', methods=['GET', 'POST'])
def handle_locations():
    if request.method == 'POST':
        return save_new_location()
    else:
        return show_all_locations()

# return 'Locations endpoint - use GET or POST actions here to add and retrieve a list of locations, or just one location'

@app.route('/locations/<int:location_id>')
def show_location(location_id):
    # return the location corresponding to the given id
    return 'Location %d' % location_id

if __name__ == '__main__':
    app.run()

