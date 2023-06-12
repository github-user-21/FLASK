from wtforms.validators import DataRequired, EqualTo, Length 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField, ValidationError
from wtforms.widgets import TextArea

# Create Form Class
class NameForm(FlaskForm):
    name = StringField("Name",validators= [DataRequired()])
    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    email = StringField("What is your Email ?",validators= [DataRequired()])
    password_hash = PasswordField("What is your Password ?",validators= [DataRequired()])
    submit = SubmitField("Submit")

#  Create Form Class
class UserForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    name = StringField("Name",validators= [DataRequired()])
    email = StringField("Email",validators= [DataRequired()])
    age = StringField("Age",validators=[DataRequired()])
    password_hash = PasswordField('Password', validators = [DataRequired(), EqualTo('password_hash2', message = 'Passwords must match')])
    password_hash2 = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    title = StringField("TITLE",validators=[DataRequired()])
    content = StringField("Content",validators=[DataRequired()], widget= TextArea())
    author = StringField("Author",validators=[DataRequired()])
    slug = StringField("Slug",validators=[DataRequired()])
    submit = SubmitField("Submit",validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Submit')
