#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request, redirect, url_for
from models import User
from definition import mongo

sample_profile = Blueprint('sample_profile', __name__, template_folder='templates')

default_selected_details = \
    {"MetaTongue": ["name", "sex", "age", "residence", "Nationality",
                    "married", "drink", "smoke"]}

@sample_profile.route('/profile', methods=['GET'])
@sample_profile.route('/<language>/profile', methods=['GET'])
def profile_backend(language):
    """

    :param language: language: Defines the language ('en' or 'cn') used for the template
    :return: The rendered samples.html template
              /samples?project=<project_name>&name=<sample_name>
    """
    if language == 'en':
         posts = { # fake array of posts
            'Home': "Home",
            'Projects': 'Projects',
            'name':'name',
            'sex':'sex',
            'age':'age',
            'residence':'residence',
            'Nationality':'Nationality',
            'married':'married',
            'drink':'drink',
            'smoke':'smoke',
            'Logout':'Logout',
            'profile':'Profile',
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
            'OK':'OK'
            }
    else:
        posts = { # fake array of posts
            'Home': U"主页",
            'Projects': U'工程',
            'name':U'姓名',
            'sex':U'性别',
            'age':U'年龄',
            'residence':U'residence',
            'Nationality':U'国籍',
            'married':U'婚姻状况',
            'drink':U'饮酒状况',
            'smoke':U'吸烟状况',
             'Logout':U'登出',
             'profile':U'个人简介',
             'Login':U'登录',
            'Register':U'注册',
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
            'OK':U'确认'
        }

    project_name = request.args.get('project', '')
    assert project_name
    assert mongo.db.projects.find({"name": project_name}).count() > 0
    sample_name = request.args.get('name', '')
    assert sample_name
    assert mongo.db.samples.find(
        {"name": sample_name, "project_name": project_name}).count() > 0
    # get sample name and project name from REQUEST
    sample_detail = mongo.db.samples.find(
        {"name": sample_name, "project_name": project_name})[0]
    selected_details = default_selected_details[project_name]
    # select certain details
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        return render_template('profile.html',language=language, posts = posts,sample_name=sample_name,
                        project_name=project_name, sample_detail=sample_detail,
                        selected_details_name=selected_details, user=user)
    return render_template('profile.html',language=language, posts = posts,sample_name=sample_name,
                           project_name=project_name, sample_detail=sample_detail,
                           selected_details_name=selected_details)
