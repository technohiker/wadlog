import os
from dotenv import load_dotenv
from re import search

from flask import Flask, render_template, request, flash, redirect, jsonify, session, g
from models import connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
        f"postgresql://{os.getenv('SQLALCHEMY_USER')}:{os.getenv('SQLALCHEMY_PASSWORD')}@{os.getenv('SQLALCHEMY_HOST')}:5432/{os.getenv('SQLALCHEMY_DATABASE')}"

       # psql -h <REMOTE HOST> -p <REMOTE PORT> -U <DB_USER> <DB_NAME>


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',"This is a secret")

connect_db(app)