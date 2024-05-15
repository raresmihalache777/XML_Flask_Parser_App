from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField

class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[
        FileRequired(),
        FileAllowed(['xml', 'json', 'dtd'], 'XML and JSON files only!')
    ])
    submit = SubmitField('Submit')