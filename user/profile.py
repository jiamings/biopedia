# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request, redirect, url_for
from models import User, StarredProjects, CreatedProjects

user_profile = Blueprint('user_profile', __name__, template_folder='templates')

@user_profile.route('/user', methods=['GET'])
@user_profile.route('/<language>/user', methods=['GET'])
def profile_backend(language='en'):

    if session['username']:
        username = session['username']
        user = User.objects.get(username=username)
        starred_projects = StarredProjects.objects(username=username)
        created_projects = CreatedProjects.objects(username=username)
        if not user['admin']:
            alert_message = request.args.get('alert_message', '')
            alert_type = request.args.get('alert_type', '')
            if alert_type:
                return render_template('user.html', user=user, disp_user=user,
                                       starred_projects=starred_projects,
                                       created_projects=created_projects,
                               language=language, alert_message=alert_message,
                               alert_type=alert_type)
            else:
                return render_template('user.html', user=user, disp_user=user,
                                       starred_projects=starred_projects,
                                       created_projects=created_projects,
                                       language=language)
        else:
            admin = user
            username = request.args.get('username', '')
            if username:
                user = User.objects.get(username=username)
            return render_template('user.html', user=admin, disp_user=user,
                                   starred_projects=starred_projects,
                                   created_projects=created_projects,
                                   language=language)

    else:
        return redirect(url_for('index.index_backend'))

@user_profile.route('/star', methods=['GET'])
def star_backend(language='en'):
    if session['username']:
        username = session['username']
        project_name = request.args.get('project', '')
        starred_project = StarredProjects.objects(username=username, project_name=project_name).count()
        if starred_project > 0:
            starred_project = StarredProjects.objects.get(username=username, project_name=project_name)
            starred_project.delete()
            return 'Star'
        else:
            starred_project = StarredProjects(username=username, project_name=project_name)
            starred_project.save()
            return 'Unstar'
    else:
        return 'Fail'


@user_profile.route('/modify-password', methods=['POST'])
@user_profile.route('/<language>/modify-password', methods=['POST'])
def modify_password(language='en'):
    password = request.form['originalPassword']
    newpassword = request.form['newPassword']
    username = session['username']
    user = User.objects.get(username=username)
    if user['password'] == password:
        User.objects(id=user.id).update_one(set__password=newpassword)
        if language == 'en':
            return redirect(url_for('.profile_backend', language="en", alert_type="alert-success", alert_message="Successfully changed password!"))
        else:
            return redirect(url_for('.profile_backend', language="cn", alert_type="alert-success", alert_message=u"修改密码成功！"))
    else:
        if language == 'en':
            return redirect(url_for('.profile_backend', language="en", alert_type="alert-danger", alert_message="Password incorrect."))
        else:
            return redirect(url_for('.profile_backend', language="cn", alert_type="alert-danger", alert_message=u"密码错误。"))