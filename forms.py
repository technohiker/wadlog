from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import InputRequired, Length

class AddCupcakeForm(FlaskForm):

    flavor = StringField('Flavor',validators=[InputRequired()])
    size = StringField('Size',validators=[InputRequired()])
    rating = FloatField('Rating(1 to 10)',validators=[InputRequired()])
    image = StringField('Image URL',validators=[InputRequired()])

class GetModsForm(FlaskForm):

    query = StringField('Search',validators=[InputRequired(),Length(min=3)])
    type = SelectField('Type',choices=[
        ['filename','Filename'],
        ['title','Title'],
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