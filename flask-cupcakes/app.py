"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, jsonify, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, update_db, delete_data, Cupcake
# from forms import AddCupcake

###################################################

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bananahammajamma'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

###################################################

@app.route('/', methods = ["GET"])
def show_cupcakes():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    return render_template('index.html')

# *****************************
# RESTFUL TODOS JSON API
# *****************************
###############################
# GET ROUTES
###############################
@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns JSON w/ all cupcakes"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Returns JSON for one cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())
###############################
# POST ROUTE
###############################

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake"""
    cupcake = Cupcake(flavor = request.json['flavor'], 
                      rating = request.json['rating'], 
                      size = request.json['size'], 
                      image = request.json['image'] or None)
    update_db(cupcake)
    response_json = jsonify(cupcake=cupcake.serialize())
    return (response_json, 201)
###############################
# PATCH ROUTE
###############################


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    """Update cupcake from data in request. Return updated data.

    Returns JSON like:
        {cupcake: [{id, flavor, rating, size, image}]}
    """
  
    json = request.json
    cupcake = Cupcake.query.get_or_404(id)
    
    cupcake.flavor = json.get('flavor', cupcake.flavor)
    cupcake.rating = json.get('rating', cupcake.rating)
    cupcake.size = json.get('size', cupcake.size)
    cupcake.image = json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())
###################################
# DELETE ROUTE
###################################

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def remove_cupcake(id):
    """Delete cupcake and return confirmation message.

    Returns JSON of {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(id)

    delete_data(cupcake)

    return jsonify(message="Deleted")
