from flask import Flask, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from secret import mq_key

import requests


URL = 'http://www.mapquestapi.com/geocoding/v1/';
key = mq_key
app = Flask(__name__);

# We want to make something like User('address':'', 'lat': ..., 'lng': ...)

@app.route('/')
def show_address_form():
    return render_template('form.html')

@app.route('/geocode')
def get_location():
  # NOTE get routes populate requests.args, post populate requests.params
  # requests.args gets populated when we click submit -> check its route!
    address = requests.args['address']
    requests.get(f"{URL}/address", params={'key':key, 'location':address})
    return render_template('form.html')