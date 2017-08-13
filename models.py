#!flask/bin/python

from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config.from_object('config')
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'meow'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    # def __init__(self, username='', email=''):
    #     self.username = username
    #     self.email = email
    # def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    def __repr__(self):
        return '<User %r>' % self.username

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, unique=True)
    embed = db.Column(db.String(5000), unique=True)
    
    # def __init__(self, num=0, embed=''):
    #     self.num = num
    #     self.embed = embed
    # def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    def __repr__(self):
        return '<Issue %d>' % self.num

admin = Admin(app, name='Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Issue, db.session))

def init_db():
    db.create_all()

    # Create a test user
    new_user = User('a@a.com', 'aaaaaaaa')
    new_user.display_name = 'Nathan'
    db.session.add(new_user)
    db.session.commit()

if __name__ == '__main__':
    init_db()

@app.route('/')
def hello_world():
    return render_template('base.html')

@app.route('/issue/<int:issue_id>')
def show_issue(issue_id):
    return render_template('issue.html', issue_id=issue_id)