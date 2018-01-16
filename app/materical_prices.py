from flask import Flask , render_template
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
moment=Moment(app)
bootstrap=Bootstrap(app)
app.config['SECRET_KEY']='mLZXlBhl7hoV39xt6PUsJI8N3UUF8r575E77953YH7hIDOv12Yw9kua4nU75xybyyFDfSM6ZO4UPW4UO69e98lisAItyUTkI2TbplZTsDdfdM9ZG'

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db=SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())
@app.route('/login')
def login():
    return  render_template('login.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__ == '__main__':
    app.run()

class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>'% self.username

