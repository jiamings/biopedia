from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask('Biopedia')
mongo = PyMongo(app)