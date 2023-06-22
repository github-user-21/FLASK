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
from webforms import LoginForm,PostForm,UserForm,PasswordForm,NameForm,SearchForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os


# Create a Flask Instance
app = Flask(__name__)

# CKEditor ::
ckeditor = CKEditor(app)

# ADD Database
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:password=aditya@localhost/users'
app.config['SECRET_KEY'] = "secretkey"


UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = ["jpg", "png", "pdf", "jpeg"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# Flask_Login Stuff
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader

def load_user(user_id):
    return Users.query.get(int(user_id))

#Create a route decorator
@app.route('/api',methods=["POST","GET"])
def api():
    favorite_character = {
        "Robert Downey Jr." : "Iron Man",
        "Tom Cruise" : "Ethan Hunt",
        "Johnny Depp" : "Captain Jack Sparrow"
    }
    return favorite_character

# Create Admin Page
@app.route("/admin")
@login_required
def admin():
    id = current_user.id
    if id == 27:
        return render_template('admin.html')
    else:
        flash("You must be Admin to access this page")
        return render_template("dashboard.html")
@app.route('/dashboard',methods = ['GET','POST'])
@login_required
def dashBoard():
    form = LoginForm(slug="username")
    return render_template('dashboard.html',form = form)

@app.route('/')

def index():
    first_name = "Aditya"
    stuff = "stuff"
    return render_template("index.html",first_name = first_name, stuff = stuff)

# localhost:5000/user/name
@app.route('/user/<name>')

def user(name):
    return render_template("user.html",user_name = name)

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

@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have Successfully Logged out!")
    return redirect(url_for('login'))


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
@login_required
def update(id):
    form = UserForm()
    name_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        name_update.username = request.form['username']
        name_update.name = request.form['name']
        name_update.email = request.form['email']
        name_update.age = request.form['age']
        name_update.about_author = request.form["about_author"]
        name_update.profile_pic = request.files['profile_pic']
        # Grab Image Name
        pic_filename = secure_filename(name_update.profile_pic.filename)
        # Set UUID
        pic_name = str(uuid.uuid1()) + "_" + pic_filename
        # Save that image
        saver = request.files['profile_pic']
        saver.save(os.path.join(app.config['UPLOAD_FOLDER']),pic_name)
        # Change it to string to save to db
        name_update.profile_pic = pic_name

        try:
            db.session.commit()
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'],pic_name))
            flash("User Updated Successfully!")
            return render_template("update.html",form = form,name_update = name_update,id = id)
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
        poster = current_user.id
        post = Posts(title = form.title.data, content = form.content.data,slug = form.slug.data,poster_id = poster)
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''

        db.session.add(post)
        db.session.commit()

        flash("Blog Post Submitted Succesfully")

    # REDIRECT to webpage
    return render_template("addpost.html",form=form)

@app.route('/posts/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = form.slug.data
        post.content = form.content.data
        # Update database
        db.session.add(post)
        db.session.commit()
        flash("Post has been edited!")

        return redirect(url_for('post',id = post.id))
    
    if current_user.id == post.poster_id:
        form.title.data = post.title
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit.html',form=form)
    else:
        flash("You are not authorised to edit this post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts = posts)
        
       
@app.route('/posts/delete/<int:id>')
@login_required
def deletepost(id):
    post_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_delete.poster.id:
        try:
            db.session.delete(post_delete)
            db.session.commit()
            posts = Posts.query.order_by(Posts.date_posted)
            flash("Post Deleted Successfully !")
            
            return render_template("posts.html",posts = posts)
        
        except:
            flash("Oops! Error!!!")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template("posts.html",posts = posts)
    else:
        flash("You are not authorised to delete this post!")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html",posts = posts)
        

@app.route('/posts')
def posts():
    # Grab all posts from database
    posts = Posts.query.order_by(Posts.date_posted)

    return render_template("posts.html",posts = posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)

    return render_template("post.html",id = id,post = post)

# Pass Stuff to Navbar
@app.context_processor
def base():
    form = SearchForm()
    return dict(form = form)


@app.route("/search",methods=['POST'])
def search():
    form = SearchForm()
    # Get data from form
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        # Query Database
        posts = posts.filter(Posts.content.like('%'+post.searched+'%'))
        posts = posts.order_by(Posts.date_posted).all()
        return render_template('search.html',form = form, searched = post.searched, posts = posts)
    
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

# Create Custom Error Pages

# 1.Invalid URL
@app.errorhandler(404)

def pagenotfound(e):
    return render_template("404.html"),404

# 2. Internal Server Error
@app.errorhandler(500)

def pagenotfound(e):
    return render_template("500.html"),500

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    # author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime,default = datetime.utcnow)
    slug = db.Column(db.String(255))
    # Foreign Key to Link Users(refer to primary id of user)
    poster_id = db.Column(db.Integer,db.ForeignKey('users.id')) 


 

# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),nullable = False, unique = True)
    name = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100),nullable = False,unique = True)
    date_added = db.Column(db.DateTime,default = datetime.utcnow)
    age = db.Column(db.Integer)
    about_author = db.Column(db.Text(255), nullable = True)
    profile_pic = db.Column(db.String(255),nullable = True)
    password_hash = db.Column(db.String(128))
    # password_hash2
        # Users can have many Posts
    posts = db.relationship("Posts", backref='poster')

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)



# Create String
def __repr__(self):
    return '<Name %r>' %self.name

# safe
# capitalize
# lower
# upper
# title
# trim
# striptags