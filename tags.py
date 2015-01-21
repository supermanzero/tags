from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.update(
SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir,'data.db'),
SQLALCHEMY_ECHO = True,
SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16',
DEBUG = True
)
# app.config.from_pyfile('hello.cfg')
db = SQLAlchemy(app)

class Tags(db.Model):
    __tablename__ = 'tags'
    id = db.Column('tags_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.TEXT)
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.now()


@app.route('/',methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     return render_template("index.html")
    return render_template("index.html",tags=Tags.query.order_by(Tags.pub_date.desc()).all())

@app.route('/add',methods=['GET', 'POST'])
def add():
    print request.referrer
    return render_template('add.html')

@app.route('/checkadd',methods=['GET', 'POST'])
def checkadd():
    if request.method == 'POST':
        if not request.form['title']:
            # flash('Title is required', 'error')
            return "error"
        elif not request.form['text']:
            # flash('Text is required', 'error')
            return "error"
        else:
            tag = Tags(request.form['title'], request.form['text'])
            db.session.add(tag)
            db.session.commit()
            # flash(u'Todo item was successfully created')
            return redirect(url_for('index'))
    else:
        return "error"


if __name__ == '__main__':
    app.run()
