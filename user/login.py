import sys
sys.path.append('../')

from flask import Blueprint, render_template, request, session, redirect, url_for
from models import User

user_login = Blueprint('user_login', __name__, template_folder='templates')

@user_login.route('/login', methods=['POST'])
@user_login.route('/<language>/login', methods=['POST'])
def login(language='en'):
    username = request.form['username']
    password = request.form['password']
    # whether we find the target username in the database or not
    user = User.objects(username=username).count()
    if user != 1:
        session['alert_place'] = 'login'
        session['alert_message'] = 'User does not exist.'
        return redirect(url_for('index.index_backend', language=language))
    else:
        user = User.objects.get(username=username)
        if user["password"] == password:
            session['username'] = username
            return redirect(url_for('index.index_backend', language=language))
        else:
            session['alert_place'] = 'login'
            session['alert_message'] = 'Password incorrect.'
            return redirect(url_for('index.index_backend', language=language))



@user_login.route('/register', methods=['POST'])
@user_login.route('/<language>/register', methods=['POST'])
def register(language='en'):
    # login information
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    num_users = User.objects(username=username).count()
    if num_users > 0:
        session['alert_place'] = 'register'
        session['alert_message'] = 'Username has been registered.'
        return redirect(url_for('index.index_backend', language=language))

    num_users = User.objects(email=email).count()
    if num_users > 0:
        session['alert_place'] = 'register'
        session['alert_message'] = 'Email has been registered.'
        return redirect(url_for('index.index_backend', language=language))

    user = User(username=username,
                password=password,
                email=email,
                firstname=firstname,
                lastname=lastname,
                admin=False)

    user.save()

    session['username'] = username
    return redirect(url_for('index.index_backend', language=language))

@user_login.route('/logout')
@user_login.route('/<language>/logout')
def logout(language='en'):
    session.pop('username', None)
    return redirect(url_for('index.index_backend', language=language))