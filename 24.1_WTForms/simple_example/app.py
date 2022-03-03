from flask import Flask, request, render_template, redirect, flash;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, update_db, delete_data

from forms import AddSnackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-wtf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True;
app.config['SECRET_KEY'] = 'murmursanmallomar';
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;
debug = DebugToolbarExtension(app)


#From models.py
connect_db(app)


temp_store = {};


@app.route('/')
def show_homepage():
  '''Renders list of all snacks'''
  return render_template('home.html')
# Pass Snack form down to template
@app.route("/add", methods=["GET", "POST"])
def add_snack():
    """Snack add form; handle adding."""

    form = AddSnackForm()

    if form.validate_on_submit():
        name = form.name.data
        price = form.price.data
        flash(f"Added {name} at {price}")
        temp_store['name'] = name
        temp_store['price'] = price
        return redirect("/")

    else:
        return render_template(
            "add_snack_form.html", form=form)