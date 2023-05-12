from flask import Flask, render_template

# Create a Flask Instance

app = Flask(__name__)

#Create a route decorator

@app.route('/')

def index():
    first_name = "A"
    stuff = "stuff"
    return render_template("index.html",first_name = first_name, stuff = stuff)

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




# def index():
#     return render_template("index.html")

# safe
# capitalize
# lower
# upper
# title
# trim
# striptags