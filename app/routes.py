from app import app
from flask import render_template

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
            'body':{'The latest movie was dope'}
        }
    ]
    return render_template('index.html',title = 'Home',user=user, posts = posts)
