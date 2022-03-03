from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
# Export this to app.py
class AddSnackForm(FlaskForm):

    """Form for adding snacks."""

    name = StringField("Snack Name")
    price = FloatField("Price in USD")

