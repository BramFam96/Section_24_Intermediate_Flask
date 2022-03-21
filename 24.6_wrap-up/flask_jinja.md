## TOC

- [Goals](#goals)
  - [Uncovered flask features](#uncovered-flask-features)
    - [url_for](#url_for)
    - [Blueprints](#blueprints)
    - [Signals](#signals)
  - [Uncovered Jinja Stuff](#uncovered-jinja-stuff)
    - [Built in Filters](#built-in-filters)
    - [Macros](#macros)
  - [Addons!](#addons)
    - [WTForms - SQLA](#wtforms---sqla)
    - [WTForms-Alchemy](#wtforms-alchemy)
    - [Flask-Login](#flask-login)
    - [flask-admin](#flask-admin)
    - [flask-mail](#flask-mail)
    - [Flask-Restless](#flask-restless)
  - [Flask vs Node-Express](#flask-vs-node-express)
  - [Flask vs Django](#flask-vs-django)

---

# Goals

---

Summarized what we've covered so far:

- Routes
- Jinja templates
- Flask-SQLAlchemy
- Flask Testing
- Cookies & Sessions
- JSON and flask
- Flask-WTForms

Get an idea for what we haven't covered:

- flask features
- jinja features
- popular add-ons
- other web frameworks

---

## Uncovered flask features

---

We did this everywhere!

```py
<a href="/users/{{ user.id }}">See user</a>
```

and

```py
def some_other_view():
    ...
    return redirect(f"/users/{user.id}")
```

What if we wanted to change that URL?

Perhaps to /profiles/[user-id]?

---

### url_for

---

Instead we do this:

```py
@app.route("/users/<int:id>")
def user_profile(id):
```

```py
<a href="{{ url_for('user_profile', id=user.id) }}">go</a>
from flask import url_for
```

```py
def some_other_view():
    ...
    redirect_url = url_for('user_profile', id=user.id)
    return redirect(redirect_url)
```

---

### Blueprints

---

Build modular “applications” in Flask:  
Import component like react:

- Each component can have own models, forms, tests, views
- Can re-use an app in many sites
  - Many sites could use the “blogly” app
- allows for larger/more complex sites

---

### Signals

---

“When [this thing] happens, do [this other] thing.”

- send an email when a user registers, no matter how they register

---

## Uncovered Jinja Stuff

---

- built in filters!
- sharing parts of templates/repeated code
- formatting of numbers, dates, lists in the template
- caching parts of templates
  - _this part only changes every 5 mins_

---

### Built in Filters

---

[Jinja docs](https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters)

Syntax:

```py
{% jinja_func|filter  %}
```

fiters include:

- max
- min
- sort(reverse= true, attribute = 'attr')
- sum(attributer='price')

---

### Macros

---

Reusable template logic:  
app/templates/macros.html:

```html
{% macro nav_link(endpoint,text) %} {% if request.endpoint.endswith(endpoint) %}
<li class="active"><a href="{{url_for(endpoint)}}">{{text}}</a></li>
{% endif %} {% endmacro %}
```

In other templates:

```html
{% from "macros.html" import nav_link with context %}
<body>
  <ul class='nav-list'>
    {{ nav_link('home','Home')}}
    {{ nav_link('about','About')}}
    {{ nav_link('contact',''Contact')}}
</body>
```

---

## Addons!

---

### WTForms - SQLA

---

Instead of this:

```py
def edit_pet(pet_id):
    pet = Pet.query.get(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.name = form.name.data
        pet.species = form.species.data
        pet.color = form.color.data
        pet.age = form.age.data
        pet.weight = form.weight.data
        pet.num_legs = form.num_legs.data
```

We do this:

```py
def edit_pet(pet_id):
    pet = Pet.query.get(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        form.populate_obj(pet)
        ...
```

---

### WTForms-Alchemy

---

Can generate WTForms from SQLAlchemy model:

```py
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from models import db, Pet, Owner

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class PetForm(ModelForm):
    class Meta:
        model = Pet

class OwnerForm(ModelForm):
    class Meta:
        model = Owner
```

---

### Flask-Login

---

Includes methods for common parts of user/passwords/login/logout

- register
- current_user
- login_user(user, remember=False, duration=None)
- logout_user
- @login_required -> simple decorator for protecting views

### flask-admin
Will generate full CRUD and an admin ui for SQLA models
### flask-mail
includes methods that generate email responses

### Flask-Restless
Does a ton of heavy lifting  
Generates CRUD API endpoints from SQLAlchemy models:
```py
from flask.restless import APIManager

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    birth_date = db.Column(db.Date)

class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    vendor = db.Column(db.Unicode)
    purchase_time = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('Person')

# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)

# API endpoints, available at /api/<tablename>
manager.create_api(User, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Computer, methods=['GET'])
# LITERALLY CREATES ALL OF OUR ROUTES
```
## Flask vs Node-Express
Pretty similar in concepts, and ideas. Both compatible with jinja templates

## Flask vs Django
Django is larger and more featurful than flask  
Far more opinionated. Django model.py:
```py
class Pet(models.Model):
  name = ...
  color = ...
  owner = models.ForeignKey("Owner")
  # assumes 'id is auto-incrementing
  # defines relationship and generates owner_id column itself
``` 
^^^ pretty cool  
**BUT THERES MORE**
```py
@app.route("/feedback/<int:feedback_id>/edit", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)
```
    
Django:
    
```py
class FeedbackEditView(generic.UpdateView):
  '''Show update-feedback form and process it'''
  model = Feedback
```
Das it.  
If Django breaks its much more difficult to diagnose and fix  
