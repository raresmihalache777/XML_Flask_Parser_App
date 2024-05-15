import os
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DTD_PATH'] = os.path.join(os.path.dirname(__file__), '../files/events.dtd')
app.config['XML_PATH'] = os.path.join(os.path.dirname(__file__), '../files/events.xml')
app.config['XML_SAVE_PATH'] = os.path.join(os.path.dirname(__file__), '../uploads')


from app import routes