from flask import Flask, render_template

# Create a Flask Instance

app = Flask(__name__)

#Create a route decorator

# @app.route('/')

# def index():
#     return "1"

# localhost:5000/user/name
@app.route('/user/<name>')

def user(name):
    return 'Hello {}'.format(name)



