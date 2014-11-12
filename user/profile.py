import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request, redirect, url_for
from models import User

user_profile = Blueprint('user_profile', __name__, template_folder='templates')

@user_profile.route('/user', methods=['GET'])
@user_profile.route('/<language>/user', methods=['GET'])
def profile_backend(language='en'):
    if session['username']:
        username = session['username']
        user = User.objects.get(username=username)
        if not user['admin']:
            alert_message = request.args.get('alert_message', '')
            alert_type = request.args.get('alert_type', '')
            if alert_type:
                return render_template('user.html', user=user, admin=user,
                               language=language, alert_message=alert_message,
                               alert_type=alert_type)
            else:
                return render_template('user.html', user=user, admin=user,
                                       language=language)
        else:
            admin = user
            username = request.args.get('username', '')
            if username:
                user = User.objects.get(username=username)
            return render_template('user.html', user=user, admin=admin,
                                   language=language)

    else:
        return redirect(url_for('index.index_backend'))


@user_profile.route('/modify-password', methods=['POST'])
def modify_password():
    password = request.form['originalPassword']
    newpassword = request.form['newPassword']
    username = session['username']
    user = User.objects.get(username=username)
    if user['password'] == password:
        User.objects(id=user.id).update_one(set__password=newpassword)
        return redirect(url_for('.profile_backend', alert_type="alert-success", alert_message="Successfully changed password!"))
    else:
        return redirect(url_for('.profile_backend', alert_type="alert-danger", alert_message="Password incorrect."))