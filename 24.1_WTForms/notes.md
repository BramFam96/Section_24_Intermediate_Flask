# WTForms

As we might guess WTForms is a python library that makes forms!  
It provides:

- Server side form validation, and feedback
- HTML production
- Security
  We can do this ourselves but it becomes very tedious!  
  Instead we'll build _classes_ for these forms

## Setup

```SQL
pip install flask-wtf
```

## Defining basic form class

```py
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
class AddSnackForm(FlaskForm):
  '''Form for adding snacks'''
  # Fields -> actually generate this html!
  name = StringField("Snack Name")
  price = FloatField("Price in USD")

```

Other fields include:

- BoolenField (checkbox)
- DateField
- DataTimeField
- IntegerField
- FloatField

## Understanding how obj based forms work:

---

Once we create class for our form we pass it to app.py

If we run our file, and a quick _dir(AddSnackForm)_ we can see the methods:

```py
 '_unbound_fields',
 '_wtforms_meta',
 'data',
 'errors',
 'hidden_tag',
 'is_submitted',
 'name',
 'populate_obj',
 'price',
 'process',
 'validate',
 'validate_on_submit'
```

Among them, **price and name** are methods we've defined  
 These methods contain **html** calls, which have our form structure ready to go!

## Rendering forms

Here we treat form as any other data and pass it along our render_template funcs:

```py
@app.route('/snacks/new')
def add_snack():
  form = AddSnackForm();
  return render_template('add_snack_form.html', form = form)
```

In add_snack_form:

```py
  <form id="snack-add_form" method ='POST'>
     {% for field in form
        if field.widget.input_value != 'hidden'%}
        <p>
          {{field.label}}
          {{field}}
        </p>
        {% endfor %}
    <button type="submit">Submit</button>
  </form>
```

Rendering a labelled form is simple as that!  
If we want to add new fields we simply add to our form class:

```py
quantity = IntegerField('Snack quantity')
```

## Security

---

Cross-site-request forgery (CSRF) refers to:  
_false form data maliciously pushed onto our POST route_  
We want to make sure that form data is coming from _our form!_
We do this with a CSRF token system.  
The token is:

- Generated from the server when a page is shown
- Included in the form HTML
- Validated by the server on form submit
  We can see this token exists by removing the line:

```py
if field.widget.input_value != 'hidden'
```

We can also add custom hidden inputs for data we want passed by default

### Luckily this heavy lifting has been done!

Using our CSRF token is a two step process:

- Include the CSRF hidden field (without showing it) (Client side)
- Validate our token on our POST route (Server side)

### Client side code:

```py
  <form id="snack-add_form" method ='POST'>
     {{form.hidden_tag() }} <!--We want this INSIDE our form element-->
     {% for field in form
        if field.widget.input_value != 'hidden'%}
```

### Server side validation

In our POST route we check if the CSRF Token is valid

```py
@app.route('/snacks/new', methods = ["GET", "POST"])
def add_snack():
  # form required for WTForms
  form = AddSnackForm();
  # checks that this is POST req AND that token is valid
    if form.validate_on_submit():
    # auto populates form with type correct data!
    name = form.name.data
    price = form.price.data

    flash(f'Added snack {name} at price {price}')
    return redirect('/add')
  else: #failed case = bad data/get req
  return render_template('add_snack_form.html', form = form)
```

it's likely we'll need different forms for adding, editing, even user priveledge  
that act on a single model

## RadioField

When we iterate over a radio field wqe get a list of subfields and need to iterate again!  
Or we'll get a crazy list of nested lis and links!  
Just use **SelectField**..

### Radio / Select -> coerce

```py
priority = SelectField('Priority Code',
choices = [(1,'High'), (2, 'Low')],
coerce = int
)
```

We do this because Radio/SelectFields will pass their data as strings  
In other field types data is automatically coerced;

## Dynamic Select Fields

We want to populate select dept with dept_codes from our DB!  
(VideoExample Form)[demo/flask-wtforms-demo/VideoDemo/form.py]:

```py
class NewEmpForm(FLaskForm):
  dept_code = SelectField('Deptartment Code')
```

Most of the heavy lifting is done in the view func:  
(VideoExample View)[demo/flask-wtforms-demo/VideoDemo/form.py]:

```py
@app.route('/employees/new')
def handle_emp_form():
  form = NewEmpForm;
  # Remember Radio/Select expects tuples!
  depts = db.session.query(Department.dept_code, Department.dept_name)
  form.dept_code.choices = depts;
```

Our form populates!

```py
%run app.py
db.session.add(Department(dept_code = 'r&d',
                          dept_name = 'Research and Development',
                          phone = '114-4312'))
db.session.commit();
```

We've got another choice!

## Out-the-box validation!

WTForms is ready to validate our inputs right out of the box!  
To do this we used the built-in _validators_

```py
from wtforms.validators import InputRequired, Optional, Email
class UserForm(FlaskForm):
  ...
  email = StringField('Email Address',
          validators= [InputRequired(message='Email Address is required'),
                       Email()])
```

Our message will override default error messaging  
Also our type specified fields are already type validated

### Looping through error responses:

```html
<!-- In the template we render fields -->
<form id="snack-add_form" method="POST">
	{{form.hidden_tag() }}
	<!--adds type-hidden form fields -->
	{% for field in form if field.widget.input_value != 'hidden'%}
	<p>
		{{field.label}} {{field}}
		<!-- Include field err with the rendering of the field -->
		{% for err in field.errors %}
		<small class="form-text text-danger"> {{err}} </small>
		{% endfor %}
	</p>
	{% endfor %}
	<button type="submit">Submit</button>
</form>
```

## Update Forms

```py
@app.route('/employees/<int:id>/edit', methods=["GET", "POST"])
def edit_employee(id):
    # Get the emp we specified:
    emp = Employee.query.get_or_404(id)
    # pass the emp to form to populate data:
    form = EmployeeForm(obj=emp)
    # We still need to provide an iterable to dept_code
    depts = db.session.query(Department.dept_code, Department.dept_name)
    form.dept_code.choices = depts

    if form.validate_on_submit():
        emp.name = form.name.data
        emp.state = form.state.data
        emp.dept_code = form.dept_code.data
        db.session.commit()
        return redirect('/phones')
    else:
        return render_template("edit_employee_form.html", form=form)

```
## Styling
---
We use *class_*
```py
{{field(class_='text-primary')}}
```
## Testing
---
For tests to work on POST routes we need to disable CSRF checking;
```py
app.config['WTF_CSRF_ENABLED'] = False
```