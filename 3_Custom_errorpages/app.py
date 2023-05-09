from flask import Flask, render_template

# Create a Flask Instance

app = Flask(__name__)

#Create a route decorator

@app.route('/')

# def index():
#     return "1"

# localhost:5000/user/name
@app.route('/user/<name>')

# def user(name):
#     return 'Hello {}'.format(name)


# Create Custom Error Pages

# 1.Invalid URL
@app.errorhandler(404)

def pagenotfound(e):
    return render_template("404.html"),404

# 2. Internal Server Error
@app.errorhandler(500)

def pagenotfound(e):
    return render_template("500.html"),500

