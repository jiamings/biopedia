from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask('Biopedia')
mongo = PyMongo(app)

ICONS_FOLDER = 'static/images/icons/'