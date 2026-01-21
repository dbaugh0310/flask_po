from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Regexp

class UploadPhoto(FlaskForm):
    zip = StringField('ZIP Code', validators=[DataRequired(), Regexp('^[0-9]{5}(?:-[0-9]{4})?$', message="Please enter a valid ZIP Code")])
    file = FileField('File')
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')