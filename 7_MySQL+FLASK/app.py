from flask import Flask, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ADD Database
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:password=aditya@localhost/users'
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

# Add Route
@app.route('/user/add',methods = ['GET','POST'])

def add():
    return render_template("add.html")