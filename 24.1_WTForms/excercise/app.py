from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, update_db, Pet
from forms import AddPetForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pets_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    """Render list of pets"""
    pets = Pet.query.all()
    return render_template("home.html", pets = pets)


# [id, name, species, photo_url, age, notes, available]
@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Renders pet form (GET) or handles pet form submission (POST)"""
    form = AddPetForm()
    if form.validate_on_submit():
        form_data = {key:value for key, value in form.data.items() if key != "csrf_token"}
        pet = Pet(form_data);
        update_db(pet)
        flash(f"{pet.name} the {pet.species} has been added to the shop.")
        return redirect('/')
    else:
        return render_template("form.html", form=form)


@app.route('/<int:pet_id>', methods=["GET", "POST"])
def edit_pet(pet_id):
    pet =  Pet.query.get_or_404(pet_id)
    form = AddPetForm()
    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.age = form.age.data
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit();
        return redirect('/')
    else:
        return render_template('form.html', form = form, pet = pet)


# @app.route('/employees/<int:id>/edit', methods=["GET", "POST"])
# def edit_employee(id):
#     emp = Employee.query.get_or_404(id)
#     form = EmployeeForm(obj=emp)
#     depts = db.session.query(Department.dept_code, Department.dept_name)
#     form.dept_code.choices = depts

#     if form.validate_on_submit():
#         emp.name = form.name.data
#         emp.state = form.state.data
#         emp.dept_code = form.dept_code.data
#         db.session.commit()
#         return redirect('/phones')
#     else:
#         return render_template("edit_employee_form.html", form=form)
