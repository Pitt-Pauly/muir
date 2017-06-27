from flask import Flask, request, json

app = Flask(__name__)

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

