from app import app
from flask import render_template, flash, redirect, url_for
from app.form import LoginForm

@app.route('/')
@app.route('/index')
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
    return render_template('index.html',title = 'Home',user=user, posts = posts)

#overiding default GET request to also accept POST requests
@app.route('/login', methods =['GET','POST'])
def login():
    form = LoginForm()
    #form.validate_on_submit does the form procressing work, gathers the data and runs all the validators
    if form.validate_on_submit():
        #Flash is a function that sends a notification to the user
        flash('Login requested for user {}, remember_me {}'.format(
        form.username.data, form.remember_me.data))
        #Redirect function instructs the client web browswer to automatically navigate to a different page
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)
