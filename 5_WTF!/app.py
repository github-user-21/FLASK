from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 

# Create a Flask Instance

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"

# Create Form Class
class NameForm(FlaskForm):
    name = StringField("What be your name, Sire ?",validators=DataRequired())
    submit = SubmitField("Submit")

# Create name page
@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = NameForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        
    return render_template("name.html",name = name,form = form)
