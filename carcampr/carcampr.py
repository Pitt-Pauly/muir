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
    USERNAME='muir',
    PASSWORD='iloveCA123' #clearly this should be changed to storing password in db using Bcrypt
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

### db helper functions end

### view definitions start

def save_new_location():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('INSERT INTO locations (name, coordinates, description) values (?, ?, ?)',
               [request.form['name'], request.form['coordinates'], request.form['description']])
    db.commit()
    flash('New location entry was successfully posted')
    return redirect(url_for('handle_locations'))

def show_all_locations():
    db = get_db()
    cur = db.execute('SELECT name, coordinates, description FROM locations ORDER BY id DESC')
    locations = cur.fetchall()
    return render_template('show_all_locations.html', locations=locations)

@app.route('/')
def hello_world():
    return 'Hello! This is the placeholder index page!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('handle_locations'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('handle_locations'))

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

### view definitions end

if __name__ == '__main__':
    app.run()

