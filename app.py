import os
from dotenv import load_dotenv
from re import search
from datetime import date
from sqlalchemy.exc import IntegrityError

import requests
import json

from flask import Flask, make_response, render_template, request, flash, redirect, jsonify, session, g
from models import connect_db, Mods, Users, db
from forms import GetModsForm, RegistrationForm, LoginForm

CURR_USER_KEY = 'current_user'

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f"postgresql://{os.getenv('SQLALCHEMY_USER')}:{os.getenv('SQLALCHEMY_PASSWORD')}@{os.getenv('SQLALCHEMY_HOST')}:5432/{os.getenv('SQLALCHEMY_DATABASE')}"

    # psql -h <REMOTE HOST> -p <REMOTE PORT> -U <DB_USER> <DB_NAME>


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',"This is a secret")

connect_db(app)

def create_mod(m_json):
    """Returns a mod record created with JSON data."""

    category = m_json['dir'].partition('/')[0]

    rating = m_json['rating'] if 'rating' in m_json else 0\

    votes = m_json['votes'] if 'votes' in m_json else 0


    return Mods(
        title=m_json['title'],
        file_id=m_json['id'],
        url=m_json['url'],
        description=m_json['description'],
        date_uploaded=m_json['date'],
        author=m_json['author'],
        category=category,
        rating=rating,
        rating_count=votes
        )

@app.before_request
def global_user():
    """Set current user to Flask's global object."""
    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/search',methods=['GET','POST'])
def front_page():
    
    form = GetModsForm()
    if (request.method == 'POST'):
        uri = 'https://www.doomworld.com/idgames/api/api.php'
        query = request.json['query']
        api_type = request.json['type']
        sort = request.json['sort']
        dir = request.json['dir']

        response = requests.get(f'{uri}?action=search&query={query}&type={api_type}&sort={sort}&dir={dir}&out=json')
        print(response.content)
        return json.loads(response.content)

    
    return render_template('search.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    """Add a new user to database."""

    if('user' in request.cookies):
        return redirect('/search')

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            new_user = Users.signup(
                username= form.username.data,
                email = form.email.data,
                password=form.password.data,
                image_url=form.image_url.data
            )
            print(Users.query.all())
            db.session.commit()
            print('Success')

            do_login(new_user)

            return redirect('/search')

        except IntegrityError:
            flash("Username already taken", 'danger')
            print('Failure')
            return render_template('register.html', form=form)
    
    return render_template('register.html',form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    if('user' in request.cookies):
        return redirect('/search')
    
    print(request)
    print(request.data)
    print(request.form)

    form = LoginForm()

    if form.validate_on_submit():
        user = Users.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Welcome, {user.username}!", "success")

            response = make_response()
            response.location = '/search'
            response.status_code = 302
            response.set_cookie('user',user.username)
            response.set_cookie('password',user.password)
            return response

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Log out user on Flask side, then return JSON to clear out LocalStorage."""

    do_logout()

    return redirect('/search')

@app.route('/api/login_status',methods=['GET'])
def login_status():
    if CURR_USER_KEY in session:
        return jsonify({"status": "True"})

    return jsonify({"status": "False"})

@app.route('/api/add_mod',methods=['POST'])
def add_mod():
    print(request)
    print(request.data)
    print(type(request.data))

    mod_data = json.loads(request.data)

    mod_check = Mods.query.filter_by(file_id=mod_data['id']).first()

    if(mod_check):
        return jsonify({
            "status": "Already pulled."
        })
    mod = create_mod(json.loads(request.data))
    db.session.add(mod)
    db.session.commit()
    return jsonify({
        "status": "Success"
    })

@app.route('/mods',methods=['GET'])
def mod_list():
    mods = Mods.query.all()
    return render_template('mods.html',mods=mods)

@app.route('/mods/<int:mod_id>',methods=['GET'])
def get_mod(mod_id):
    mod = Mods.query.get(mod_id)
    print(mod)
    print(g.user.user_mods)
    print(mod in g.user.user_mods)
    return render_template('mod.html',mod=mod)