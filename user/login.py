import sys
sys.path.append('../')

from flask import Blueprint, render_template, request, session, redirect, url_for
from models import User

user_login = Blueprint('user_login', __name__, template_folder='templates')

@user_login.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # whether we find the target username in the database or not
    user = User.objects.get(username=username)
    if user:
        if user["password"] == password:
            session['username'] = username
            return redirect(url_for('index.index_backend'))
        else:
            return redirect(url_for('index.index_backend', alert_place="login", alert_message="Password incorrect."))
    else:
        return redirect(url_for('index.index_backend', alert_place="login", alert_message="User does not exist."))


@user_login.route('/register', methods=['POST'])
def register():
    # login information
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    num_users = User.objects(username=username).count()
    if num_users > 0:
        return redirect(url_for('index.index_backend', alert_place="register", alert_message="Username has been registered."))

    num_users = User.objects(email=email).count()
    if num_users > 0:
        return redirect(url_for('index.index_backend', alert_place="register", alert_message="Email has been registered."))

    user = User(username=username,
                password=password,
                email=email,
                firstname=firstname,
                lastname=lastname,
                admin=False)

    user.save()

    session['username'] = username
    return redirect(url_for('index.index_backend'))

@user_login.route('/logout')
@user_login.route('/<language>/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index.index_backend'))