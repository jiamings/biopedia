import sys
sys.path.append('../')

from flask import Blueprint, render_template, request, session
from models import User

index = Blueprint('index', __name__, template_folder='templates')

@index.route('/')
@index.route('/index')
@index.route('/<language>/index')
def index_backend(language='en'):
    """
    Returns the index page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered index.html template, which currently contains almost nothing.
    """
    alert_place = request.args.get('alert_place', '')
    alert_message = request.args.get('alert_message', '')
    if alert_message and alert_place:
        return render_template('index.html', language=language, alert_place=alert_place, alert_message=alert_message)
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        return render_template('index.html', language=language, user=user)
    return render_template('index.html', language=language)