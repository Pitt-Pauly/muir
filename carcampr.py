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
    DATABASE=os.path.join(app.root_path, '/data/db.sqlite'),
    SECRET_KEY='93WQPOOX8VO49uf5Sy0xIMgwSh7KmaPWR2tr',
    USERNAME='muir',
    PASSWORD='default'
))
app.config.from_envvar('CARCAMP_SETTINGS', silent=True)

### app config end

### db helper functions start

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

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

