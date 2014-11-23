#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
sys.path.append('../')

from flask import Blueprint, render_template, request, session, send_file
from models import User
from definition import app
from indexLanguage import Language

index = Blueprint('index', __name__, template_folder='templates')
counter = 0

@index.route('/index')
@index.route('/<language>/index')
def index_backend(language='en'):
    global counter
    counter = counter + 1
    """
    Returns the index page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered index.html template, which currently contains almost nothing.
    """
    #alert_place = request.args.get('alert_place', '')
    #alert_message = request.args.get('alert_message', '')

    lang = Language()
    if language == 'cn':
        posts = lang.selectLanguage('cn')
    else:
        posts = lang.selectLanguage('en')
        
    if 'alert_message' in session and 'alert_place' in session:
        alert_message = session['alert_message']
        alert_place = session['alert_place']
        session.pop('alert_message', None)
        session.pop('alert_place', None)
        return render_template('index.html', counter=counter, posts = posts,language=language, alert_place=alert_place, alert_message=alert_message)
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        return render_template('index.html', counter=counter, posts = posts,language=language, user=user)
    return render_template('index.html', counter=counter, posts = posts, language=language)

@index.route('/random-picture', methods=['GET'])
def random_picture(language='en'):
    project_name = request.args.get('project_name', '')
    alphabet = project_name[0].lower()
    filename = 'static/images/icons/appbar.scrabble.' + alphabet + '.png'
    return send_file(filename, mimetype='image/png')

@index.route('/star-picture', methods=['GET'])
def star_picture():
    return send_file('static/images/icons/appbar.star.add.png', mimetype='image/png')

@index.route('/unstar-picture', methods=['GET'])
def unstar_picture():
    return send_file('static/images/icons/appbar.star.delete.png', mimetype='image/png')