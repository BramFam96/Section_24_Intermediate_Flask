from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField, SelectField
from wtforms.validators import InputRequired, URL, Length, Optional, NumberRange


class AddPetForm(FlaskForm):
    name = StringField(
      "Name", 
      validators=[InputRequired(message="Pet must have a name!")],)
    species = SelectField(
    "Species",
    choices =[('cat','Cat'), ('dog','Dog'),('porcupine','Porcupine')],  
    validators=[InputRequired(message="Pet must have a species!")],
    )
    photo_url = StringField(
      "Link to Photo", 
      validators=[Optional(), URL()],
    )
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=25)], )
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=250)],)


    
    available = BooleanField("Available for adoption?")