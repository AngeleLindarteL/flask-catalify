from flask_wtf import FlaskForm
from wtforms import validators, StringField
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    title = StringField('Titulo de La Pelicula', validators=[DataRequired()])
    descripcion = StringField('Descripción de la Pelicula', validators=[DataRequired()])
    imglink = StringField('Link de la Imagen', validators=[DataRequired()])