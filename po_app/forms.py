from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Regexp

class POForm(FlaskForm):
    zip = StringField('ZIP Code', validators=[DataRequired(), Regexp('^[0-9]{5}(?:-[0-9]{4})?$', message="Please enter a valid ZIP Code")])
    city = StringField('City', validators=[DataRequired()])
    visited = BooleanField('Visited')
    submit = SubmitField('Submit')