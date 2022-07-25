from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FloatField
from wtforms.validators import InputRequired

class AddCupcakeForm(FlaskForm):

    __tablename__ = 'Cupcakes'

    flavor = StringField('Flavor',validators=[InputRequired()])
    size = StringField('Size',validators=[InputRequired()])
    rating = FloatField('Rating(1 to 10)',validators=[InputRequired()])
    image = StringField('Image URL',validators=[InputRequired()])