import json
from dis import Positions

from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
local_server = params["local_server"]

app = Flask(__name__)
app.secret_key = 'supersecretkey'

if local_server == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = params["local_uri"]
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["prod_uri"]

db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.String(120), unique=False, nullable=False)
    message = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.String(12), unique=False, nullable=True)

class Thought(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    title = db.Column(db.String(120), unique=False, nullable=False)
    content = db.Column(db.String(120), unique=False, nullable=False)
    slug = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.String(12), unique=False, nullable=True)
    img_file = db.Column(db.String(20), unique=False, nullable=True)


@app.route("/", methods = ['GET', 'POST'])
def home():
    thoughts = Thought.query.all()
    if 'user' in session and session['user'] == params['username']:
        return render_template("dashboard.html", thoughts = thoughts)

    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')

        if username == params['username'] and userpass == params['userpassword']:
            session['user'] = username
            return render_template("dashboard.html", thoughts = thoughts)
    else:
        return render_template('home.html', params = params)

@app.route("/index")
def index():
    thought = Thought.query.filter_by().all()

    return render_template('index.html', thoughts = thought)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():

    if(request.method == 'POST'):

        name = request.form.get('name')
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        message = request.form.get('msg')
        entry = Contacts(name = name, email = email, phone = phone_num, date = datetime.now(), message = message)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')

@app.route("/post/<string:post_slug>", methods =['GET'])
def post(post_slug):
    fetched_post = Thought.query.filter_by(slug = post_slug).first()

    return render_template('post.html', fetched_post = fetched_post)

app.run(debug = True)

