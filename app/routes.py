from app import app
from flask import render_template, flash, redirect, request, url_for #html display and navigation
from app.form import LoginForm #form for logins
from flask_login import current_user, login_user,logout_user , login_required #handles user login, identifying which user
from werkzeug.urls import url_parse
from app.models import User
from app.form import RegistrationForm

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'Anthony'}
    posts = [
        {
            'author':{'username':'John'},
            'body':'Beautiful Day in Santa Barbara'
        },
        {
            'author':{'username':'Apple'},
            'body':'The latest movie was dope'
        }
    ]
    return render_template('index.html',title = 'Home', posts = posts)

#overiding default GET request to also accept POST requests
@app.route('/login', methods =['GET','POST'])
def login():
    #check if the user is already authenticated; no need to user to authenicate twice
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    #form.validate_on_submit does the form procressing work, gathers the data and runs all the validators
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or user.check_password(form.password.data):
            #Flash is a function that sends a notification to the user across different webpages
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        #Redirect function instructs the client web browswer to automatically navigate to a different page
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    #returns the first value or 404 error if nothing is found
    user = User.query.filter_by(username=username).first_or_404()
    posts=[
        {"author":user,'body':'Test post #1'}
        {'author':user,'body':'Test post #2'}
    ]
    return render_template('user.html',user= user, posts = posts)
