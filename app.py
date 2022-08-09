import os
from dotenv import load_dotenv
from re import search
from datetime import date
from sqlalchemy.exc import IntegrityError

import requests
import json

from flask import Flask, make_response, render_template, request, flash, redirect, jsonify, session, g
from models import Records, connect_db, Mods, Users, Logs, db, Comments
from forms import GetModsForm, RegistrationForm, LoginForm, RecordForm

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

@app.before_first_request
def check_cookies():
    if('user' in request.cookies):
        user = Users.query.filter_by(username=request.cookies['user']).first()
        if(user):
            do_login(user)
    else:
        do_logout()

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
            db.session.commit()

            do_login(new_user)

            response = make_response()
            response.location = '/search'
            response.status_code = 302
            response.set_cookie('user',new_user.username)
            response.set_cookie('password',new_user.password)
            return response

        except IntegrityError:
            flash("Username already taken", 'danger')
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

@app.route('/logout',methods=['POST'])
def logout():
    """Log out user on Flask side, then return JSON to clear out LocalStorage."""

    do_logout()

    response = make_response()
    response.delete_cookie('user')
    response.delete_cookie('password')
    response.location = '/search'
    response.status_code = 302

    return response

@app.route('/api/login_status',methods=['GET'])
def login_status():
    if CURR_USER_KEY in session:
        return jsonify({"status": "True"})

    return jsonify({"status": "False"})

###########################################
# Mods

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

@app.route('/mods/<int:mod_id>',methods=['GET','POST'])
def get_mod(mod_id):
    
    mod = Mods.query.get(mod_id)
    print(mod in g.user.records)
    print([record.mod_id for record in g.user.records])
    if(request.method == 'POST'):
        if(g.user):
            record = Records(user_id=g.user.id,mod_id=mod_id)
            print("User Mods: ",g.user.records)

            try:
                db.session.add(record)
                db.session.commit()
                flash('Mod successfully added!')
            except IntegrityError as e:
                flash('This mod is already in your records.')
                db.session.rollback()


    return render_template('mod.html',mod=mod, IDs = [record.mod_id for record in g.user.records])

###########################################
# Records
@app.route('/mods/<int:mod_id>/delete',methods=['POST'])
def remove_record(mod_id):
    if(g.user):
        Records.query.filter_by(mod_id=mod_id,user_id=g.user.id).delete()
    redirect(f'/mods/{mod_id}')

@app.route('/records',methods=['GET'])
def record_list():
    records = Records.query.all()
    return render_template('records.html',records=records)

@app.route('/records/<int:record_id>',methods=['GET'])
def get_record(record_id):
    record = Records.query.get(record_id)
    return render_template('record.html',record=record)

@app.route('/records/<int:record_id>/edit',methods=['GET','POST'])
def edit_record(record_id):
    record = Records.query.get(record_id)
    form = RecordForm(obj=record)

    if form.validate_on_submit():
        record.user_notes = form.user_notes.data
        record.review = form.review.data
        record.now_playing = form.now_playing.data
        record.user_notes = form.user_notes.data

        db.session.add(record)
        db.session.commit()
    
        return redirect(f'/records/{record_id}')

    return render_template('record_edit.html',form=form)

@app.route('/records/<int:record_id>',methods=['POST'])
def delete_record(record_id):
    mod_id = Records.query.filter_by(id=record_id).first().mod_id
    if(g.user):
        Records.query.filter_by(id=record_id).delete()
    redirect(f'/mods/{mod_id}')

#########################################################
# Users

@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    user = Users.query.get(user_id)
    comments = Comments.query.filter_by(target_user=user_id)
    return render_template('user.html',user=user,comments=comments)

@app.route('/users/<int:user_id>/edit',methods=['GET','POST'])
def edit_user(user_id):
    user = Users.query.get(user_id).first()
    return render_template('user_edit.html',user=user)

#########################################################
# Comments

@app.route('/api/comments/add',methods=['POST'])
def add_comment():
    data = json.loads(request.data)
    comment = Comments(user_id=g.user.id,target_user=data['target_user'],text=data['comment'])
    db.session.add(comment)
    db.session.commit()
    print(data)
    return jsonify(comment.serialize())