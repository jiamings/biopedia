# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request, redirect, url_for
from models import User, StarredProjects, CreatedProjects

user_profile = Blueprint('user_profile', __name__, template_folder='templates')

@user_profile.route('/user', methods=['GET'])
@user_profile.route('/<language>/user', methods=['GET'])
def profile_backend(language='en'):
    if language == 'en':
        posts = { # fake array of posts
            'Home': "Home",
            'Projects': 'Projects',
            'Biopedia': 'Biopedia',
            'Login':'Login',
            'Register':'Register',
            'login_title':'Login with Biopedia Account',
            'username':'Username',
            'Password':'Password',
            'CLOSE':'close',
            'regi_title':'Register New Biopedia Account',
            'name_First':'First Name',
            'name_Last':'Last Name',
            'Email':'Email',
            'con_password':'Confirm Password',
            'Star':'Star',
            'Delete':'Delete',
            'M_F':'Mapping File',
            'S_F':'Sample File',
            'OK':'OK',
            'pro_title':'Biopedia - Projects',
            'User_info':'User Information',
            'Full_name':'Full Name',
            'mdf_pass':'MODIFY PASSWORD',
            'star_pro':'Starred Projects',
            'new_pass':'New Password',
            'modify':'MODIFY',
            'create_Project':'Created Projects',
            'Desprition':'We need a description for every project.',
            'U_Profile':'User Profile',
            'Logout':'Logout',
            'profile':'Profile'
        }
    else:
        posts = { # fake array of posts
            'Home': U"主页",
            'Projects': U'项目',
            'Biopedia': U'未命名',
            'Login':U'登录',
            'Register':U'注册',
            'title':U'在线生物信息学数据中心-Biopedia',
            'login_title':U'使用Biopedia账号登录',
            'username':U'用户名',
            'Password':U'密码',
            'CLOSE':U'关闭',
            'regi_title':U'注册新的Biopedia账号',
            'name_First':U'名',
            'name_Last':U'姓',
            'Email':U'电子邮件',
            'con_password':U'确认密码',
            'Star':U'赞',
            'Delete':U'取消',
            'M_F':U'映像文件',
            'S_F':U'样本文件',
            'OK':U'确认',
            'pro_title':U'Biopedia-项目',
            'User_info':U'用户信息',
            'Full_name':U'全名',
            'mdf_pass':U'修改密码',
            'star_pro':U'喜欢的项目',
            'new_pass':U'新密码',
            'modify':U'修改',
            'create_Project':U'创建的项目',
            'Desprition':U'请描述你的项目。',
            'U_Profile':U'个人信息',
             'Logout':U'登出',
             'profile':U'个人简介'
        }
    if session['username']:
        username = session['username']
        user = User.objects.get(username=username)
        starred_projects = StarredProjects.objects(username=username)
        created_projects = CreatedProjects.objects(username=username)
        if not user['admin']:
            alert_message = request.args.get('alert_message', '')
            alert_type = request.args.get('alert_type', '')
            if alert_type:
                return render_template('user.html', user=user, posts = posts, disp_user=user,
                                       starred_projects=starred_projects,
                                       created_projects=created_projects,
                               language=language, alert_message=alert_message,
                               alert_type=alert_type)
            else:
                return render_template('user.html', user=user, posts = posts,disp_user=user,
                                       starred_projects=starred_projects,
                                       created_projects=created_projects,
                                       language=language)
        else:
            admin = user
            username = request.args.get('username', '')
            if username:
                user = User.objects.get(username=username)
            return render_template('user.html', user=admin, posts = posts,disp_user=user,
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