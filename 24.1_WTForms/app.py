from flask import Flask, request, render_template, redirect, flash;
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, update_db, delete_data,

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True;
app.config['SECRET_KEY'] = 'murmursanmallomar';
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False;
debug = DebugToolbarExtension(app)


#From models.py
connect_db(app)

@app.route('/users')
def show_user_list():
  '''Renders list of all users'''
  return render_template('users/user-list.html', users = users)