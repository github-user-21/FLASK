from flask import Flask, render_template,flash,request,redirect,url_for
from wtforms.validators import DataRequired, EqualTo, Length 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField, ValidationError
from wtforms.widgets import TextArea
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, UserMixin, LoginManager, logout_user, current_user


# Create a Flask Instance
app = Flask(__name__)

# ADD Database
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:password=aditya@localhost/users'
app.config['SECRET_KEY'] = "secretkey"

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

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

# Flask_Login Stuff
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader

def load_user(user_id):
    return Users.query.get(int(user_id))

# Create a Blog Post Model
class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime,default = datetime.utcnow)
    slug = db.Column(db.String(255))


# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),nullable = False, unique = True)
    name = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100),nullable = False,unique = True)
    date_added = db.Column(db.DateTime,default = datetime.utcnow)
    age = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    # password_hash2

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

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

@app.route('/api',methods=["POST","GET"])
def api():
    favorite_character = {
        "Robert Downey Jr." : "Iron Man",
        "Tom Cruise" : "Ethan Hunt",
        "Johnny Depp" : "Captain Jack Sparrow"
    }
    return favorite_character
    # return 

# Create password test page
@app.route('/test',methods=['GET','POST'])
def test():
    email = None
    password = None
    pw_check = None
    passed = None
    form = PasswordForm()
    # Validate Form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data

        form.email.data = ''
        form.password_hash.data = ''

        pw_check = Users.query.filter_by(email=email).first()
        # check password
        passed = check_password_hash(pw_check.password_hash,password)
        # flash("Form Submitted Successfully!!")
        
    return render_template("test.html",email = email,password = password, pw_check = pw_check,passed = passed,form = form)


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
    form = UserForm()
    our_users = Users.query.order_by(Users.date_added)
    # Validate Form
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            # Hash Password!
            hashed_pw = generate_password_hash(form.password_hash.data,"sha256")
            user = Users(username = form.username.data, name = form.name.data,email = form.email.data,age=form.age.data, password_hash = hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.username.data = ''
        form.name.data = ''
        form.email.data = ''
        form.age.data = ''
        form.password_hash.data = ''

        flash("Form Submitted Successfully!!")
    return render_template('add.html',form = form,name = name, our_users = our_users)

# Update Database Record
@app.route('/update/<int:id>',methods=['GET','POST'])

def update(id):
    form = UserForm()
    name_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_update.username = request.form['username']
        name_update.name = request.form['name']
        name_update.email = request.form['email']
        name_update.age = request.form['age']
       
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",form = form,name_update = name_update)
        except:
             flash("Error! Try Again!")
             return render_template("update.html",form = form,name_update = name_update)
    else:
        return render_template("update.html",form = form,name_update = name_update,id = id)
    
@app.route('/delete/<int:id>')

def delete(id):
    name = None
    form = UserForm()
    user_delete = Users.query.get_or_404(id)

    try:
        db.session.delete(user_delete)
        db.session.commit()
        our_users = Users.query.order_by(Users.date_added)
        flash("User Deleted Successfully !")
        return render_template("add.html",form = form,name = name, our_users = our_users)
    
    except:
        flash("Oops! Error!!!")
        return render_template("add.html",form = form,name = name, our_users = our_users)

@app.route('/add-post',methods = ['GET','POST'])
# @login_required
def addpost():
    form = PostForm()


    if form.validate_on_submit():
        post = Posts(title = form.title.data, content = form.content.data,slug = form.slug.data,author = form.author.data)
        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        form.slug.data = ''

        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submitted Succesfully")

    # REDIRECT to webpage
    return render_template("addpost.html",form=form)

@app.route('/posts')
def posts():
    # Grab all posts from database
    posts = Posts.query.order_by(Posts.date_posted)

    return render_template("posts.html",posts = posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)

    return render_template("post.html",id = id,post = post)

@app.route('/posts/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update database
        db.session.add(post)
        db.session.commit()
        flash("Post has been edited!")

        return redirect(url_for('post',id = post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit.html',form=form)

@app.route('/posts/delete/<int:id>')
def deletepost(id):
    post_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_delete)
        db.session.commit()
        posts = Posts.query.order_by(Posts.date_posted)
        flash("Posts Deleted Successfully !")
        
        return render_template("posts.html",posts = posts)
    
    except:
        flash("Oops! Error!!!")
        return render_template("posts.html",posts = posts)

# Create login page

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # Check Hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successful!")
                return redirect(url_for('dashBoard'))
            else:
                flash("Incorrect Password!,Try Again")
        else:
            flash("User Doesn't Exist :(")

    return render_template ('login.html',form = form)    
    
@app.route('/dashboard',methods = ['GET','POST'])
@login_required
def dashBoard():
    form = LoginForm(slug="username")
    return render_template('dashboard.html',form = form)

@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have Successfully Logged out!")
    return redirect(url_for('login'))



# Create String
def __repr__(self):
    return '<Name %r>' %self.name