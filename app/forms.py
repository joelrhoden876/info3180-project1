from flask_wtf import FlaskForm
# from flask_uploads import UploadSet, IMAGES
from wtforms import StringField, PasswordField, FileField, TextAreaField, SelectField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class PropertyForm(FlaskForm):
    # username = StringField('Username', validators=[InputRequired()])
    # password = PasswordField('Password', validators=[InputRequired()])
    title = StringField('Property Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    rooms = StringField('No. of Rooms', validators=[InputRequired()])
    bathrooms = StringField('No. of Bathrooms', validators=[InputRequired()])
    price = StringField('Price', validators=[InputRequired()])
    type = SelectField(u'Property Type', choices=[('Apartment'), ('House')])
    location = StringField('Location', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'png', 'Images only!'])])