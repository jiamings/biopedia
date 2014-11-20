#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
sys.path.append('../')

from flask import Blueprint, render_template, request, session, send_file
from models import User
from definition import app

index = Blueprint('index', __name__, template_folder='templates')
counter = 0

@index.route('/index')
@index.route('/<language>/index')
def index_backend(language='en'):
    """
    Returns the index page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered index.html template, which currently contains almost nothing.
    """
    #alert_place = request.args.get('alert_place', '')
    #alert_message = request.args.get('alert_message', '')
    if language != 'cn':
        posts = { # fake array of posts
            'Home': "Home",
            'Projects': 'Projects',
            'Biopedia': 'Biopedia',
            'comment': 'This is the index page for Biopedia.',
            'Learn': 'Learn more',
            'Preprocessors': 'Preprocessors',
            'pre_comment1':'Bootstrap ships with vanilla CSS, but its source code utilizes the two most popular CSS preprocessors, ',
            'Less':'Less',
            'and': ' and ',
            'Sass':'Sass',
            'pre_comment2':'. Quickly get started with precompiled CSS or build on the source.',
            'One': 'One framework, every device.',
            'One_comment':'Bootstrap easily and efficiently scales your websites and applications with a single code base, from phones to tablets to desktops with CSS media queries.',
            'Full':'Full of features',
            'Full_comment':'With Bootstrap, you get extensive and beautiful documentation for common HTML elements, dozens of custom HTML and CSS components, and awesome jQuery plugins.',
            'title':'Online Bioinformatics Data Center - Biopedia',
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
            'profile':'Profile',
            'upload_data':'Upload Data',
            'Logout':'Logout'
        }
    else:
        posts = { # fake array of posts
            'Home': U"主页",
            'Projects': U'工程',
            'Biopedia': U'Biopedia',
            'comment': U'这是Biopedia的索引页',
            'Learn': U'了解更多...',
            'Preprocessors': U'预处理器',
            'pre_comment1':U'Bootstrap基于vanilla CSS,但是它的源码利用了两个最常用的预处理器，',
            'Less':'Less',
            'and' : U' 和 ',
            'Sass':'Sass',
            'pre_comment2':U'。快速使用precompiled CSS 或者在源上建立项目。',
            'One': U'适用于所有设备的网络开发框架',
            'One_comment':U'从电话到平板电脑到虚拟桌面，使用CSS media queries，Bootstrap 简单、有效的构建你的网站和应用。',
            'Full':U'包含所有特性',
            'Full_comment':U'使用Bootstrap, 你可以得到对常用网页设计、大量的常见HTML和CSS components以及极好的jQuery plugins进行拓展且漂亮的文档。',
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
            'profile':U'个人简介',
            'upload_data':U'上传数据',
            'Logout':U'登出'
        }
    if 'alert_message' in session and 'alert_place' in session:
        alert_message = session['alert_message']
        alert_place = session['alert_place']
        session.pop('alert_message', None)
        session.pop('alert_place', None)
        return render_template('index.html', posts = posts,language=language, alert_place=alert_place, alert_message=alert_message)
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        return render_template('index.html', posts = posts,language=language, user=user)
    return render_template('index.html', posts = posts,language=language)

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