from ast import Pass
import email
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField, EmailField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Email

class AddCupcakeForm(FlaskForm):

    flavor = StringField('Flavor',validators=[InputRequired()])
    size = StringField('Size',validators=[InputRequired()])
    rating = FloatField('Rating(1 to 10)',validators=[InputRequired()])
    image = StringField('Image URL',validators=[InputRequired()])

class RegistrationForm(FlaskForm):

    email = EmailField('E-mail',validators=[InputRequired(),Email()])
    username = StringField('Username',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])
    image_url = StringField('Profile Picture URL')

class LoginForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class GetModsForm(FlaskForm):

    query = StringField('Search',validators=[InputRequired(),Length(min=3)])
    type = SelectField('Type',choices=[
        ['title','Title'],
        ['filename','Filename'],
        ['author','Author'],
        ['e-mail','E-mail'],
        ['description','Description'],
        ['credits','Credits'],
        ['editors','Editors'],
        ['whole textfile','Whole_textfile']
    ])
    sort = SelectField('Sort',choices=[
        ['date','Date'],
        ['filename','Filename'],
        ['author','Author'],
        ['title','Title'],
        ['size','Size'],
        ['rating','Rating']
        ])
    dir = SelectField('Direction',choices=[['asc', 'Asc'],['desc','Desc']])

class RecordForm(FlaskForm):
    user_review = TextAreaField('Review')
    user_notes = StringField('Notes')
    play_status = SelectField('Play Status',choices=[
        ['unplayed','Unplayed'],
        ['played','Played'],
        ['beaten','Beaten']
    ])
    now_playing = BooleanField('Now Playing')