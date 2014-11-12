import sys
sys.path.append('../')

from flask import Blueprint, render_template, request, session, redirect, url_for
from models import User

user_admin = Blueprint('user_admin', __name__, template_folder='templates')

@user_admin.route('/user-admin')
@user_admin.route('/<language>/user-admin')
def user_admin_backend(language='en'):
    if session['username']:
        username = session['username']
        user = User.objects.get(username=username)
        if not user['admin']:
            return redirect(url_for('index'))
        else:
            users_list = User.objects()
            return render_template('user-admin.html', user=user, language=language, users_list=users_list)
    else:
        return redirect(url_for('index'))

@user_admin.route('/delete-user')
def delete_user():
    username = request.args.get('username', '')
    user = User.objects.get(username=username)
    if user:
        user.delete()
    return redirect(url_for('.user_admin_backend'))