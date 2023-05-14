from flask import Flask, render_template,flash
from wtforms.validators import DataRequired 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)

# ADD Database
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:password=aditya@localhost/users'
app.config['SECRET_KEY'] = "secretkey"

# Initialize database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100),nullable = False,unique = True)
    date_added = db.Column(db.DateTime,default = datetime.utcnow)


# Create String
def __repr__(self):
    return '<Name %r>' %self.name

#Create a route decorator

@app.route('/')

def index():
    first_name = "Aditya"
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
    name = StringField("Name",validators= [DataRequired()])
    submit = SubmitField("Submit")

#  Create Form Class
class UserForm(FlaskForm):
    name = StringField("Name",validators= [DataRequired()])
    email = StringField("Email",validators= [DataRequired()])
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

@app.route('/user/add',methods = ['GET','POST'])

def add():
    name = None
    our_user = None
    form = UserForm()
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name = form.name.data,email = form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("Form Submitted Successfully!!")
        our_user = Users.query.order_by(Users.date_added)
    return render_template('add.html',form = form,name = name,our_user = our_user)