import os
from dotenv import load_dotenv
from re import search
from datetime import date

import requests
import json

from flask import Flask, render_template, request, flash, redirect, jsonify, session, g
from models import connect_db, Mods, db
from forms import GetModsForm

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

    return Mods(
        title=m_json['title'],
        file_id=m_json['id'],
        url=m_json['url'],
        description=m_json['description'],
        date_uploaded=m_json['date'],
        author=m_json['author'],
        category=category,
        rating=m_json['rating'],
        rating_count=m_json['votes']
        )

# uri = 'https://www.doomworld.com/idgames/api/api.php'
# query = 'hell revealed'
# api_type = 'title'
# sort = 'asc'

# response = requests.get(f'{uri}?action=search&query={query}&type={api_type}&dir={sort}&out=json')

# data = str(response.content)

# json_data = json.loads(response.content)
# print(json_data['content']['file'][0]['dir'].partition('/')[0])

# hr_e1 = json_data['content']['file'][0]

# new_mod = create_mod(hr_e1)

# db.session.add(new_mod)
# db.session.commit()


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