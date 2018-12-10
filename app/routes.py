from app import app, db
from flask import render_template, flash, redirect, request, url_for #html display and navigation
from app.form import LoginForm #form for logins
from flask_login import current_user, login_user,logout_user , login_required #handles user login, identifying which user
from werkzeug.urls import url_parse
from app.models import User, Post
from app.form import RegistrationForm, EditProfileForm, PostForm
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods = ['GET','POST'])
@app.route('/index', methods = ['GET','POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author = current_user)
        print(form.post.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page',1,type = int)
    posts = current_user.followed_posts().paginate(page,app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page = posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page = posts.prev_num) if posts.has_prev else None
    return render_template('index.html',title = 'Home Page',form = form, posts = posts.items, next_url = next_url, prev_url = prev_url)

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
        if user is None or not user.check_password(form.password.data):
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
    page = user.post.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'])
    return render_template('user.html',user= user, posts = posts)

@app.route('/edit_profile', methods = ['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved")
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title = 'Edit Profile', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You can not follow yourself!')
        return redirect(url_for('user',username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user',username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You can not unfollow yourself!')
        return redirect(url_for('user',username = username))
    current_user.unfollow(user)
    db.session.commit()
    flash('Ypu are not following {}'.format(username))
    return redirect(url_for('user',username=username))

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page',1,type = int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page = posts.next_num) if posts.has_next else None
    prev_url = url_for('explore', page = posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title = 'Explore', posts=posts.items, next_url = next_url, prev_url = prev_url)
