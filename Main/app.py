from flask import Flask, render_template,flash
from wtforms.validators import DataRequired 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 

# Create a Flask Instance

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"

#Create a route decorator

@app.route('/')

def index():
    first_name = "A"
    stuff = "stuff"
    return render_template("index.html",first_name = first_name, stuff = stuff)

# def index():
#     return render_template("index.html")

# safe
# capitalize
# lower
# upper
# title
# trim
# striptags


# localhost:5000/user/name
@app.route('/user/<name>')

def user(name):
    return render_template("user.html",user_name = name)

# Create Custom Error Pages

# 1.Invalid URL
@app.errorhandler(404)

def pagenotfound(e):
    return render_template("404.html"),404

# 2. Internal Server Error
@app.errorhandler(500)

def pagenotfound(e):
    return render_template("500.html"),500

# Create Form Class
class NameForm(FlaskForm):
    name = StringField("What be your name, Sire ?",validators= [DataRequired()])
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
        flash("Form Submitted Successfully!!")
        
    return render_template("name.html",name = name,form = form)
