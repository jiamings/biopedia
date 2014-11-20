#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request
from models import User
from definition import mongo
import os

samples = Blueprint('samples', __name__, template_folder='templates')

default_selected_fields = \
    {"MetaTongue": ["sex", "age", "residence", "Nationality",
                    "married", "drink", "smoke"]}

default_fields_string_type = {
    "MetaTongue": ["sex", "residence", "Nationality", "tongueColor"]}


@samples.route('/<language>/samples', methods=['GET'])
def samples_backend(language):
    """
    Returns the sample page.
    :param language: Defines the language ('en' or 'cn') used for the template
    :return: The rendered samples.html template
              /samples?name=<project_name>
    """
    project_name = request.args.get('name', '')
    assert project_name
    assert mongo.db.projects.find({"name": project_name}).count() > 0
    assert mongo.db.samples.find({"project_name": project_name}).count() > 0
    sample_list = mongo.db.samples.find({"project_name": project_name})
    if request.args.get("fields", ''):
        project_fields_name = request.args.getlist("fields")
    else:
        assert mongo.db.fields.find({"project_name": project_name}).count() > 0
        project_fields_name = mongo.db.fields.find({"project_name": project_name})[0]["default_fields"]
    # to take the keys of one of the sample as heads of the sample table
    all_fields_name = dict(sample_list[0]).keys()
    all_fields_name.remove("_id")
    all_fields_name.remove("project_name")
    all_fields_name.sort()
    # get all the fields (for more fields)
    assert mongo.db.fields.find({"project_name": project_name}).count() > 0
    fields_string_type = mongo.db.fields.find({"project_name": project_name})[0]["string_fields"]

    string_field_element = {}

    for sample in sample_list:
        for field in fields_string_type:
            if not string_field_element.has_key(field):
                string_field_element[field] = []
            string_field_element[field].append(sample[field])
    # to get possible value of keys

    print request.args

    filter = {"project_name": project_name}
    for field in project_fields_name:
        if field in fields_string_type:
            value = request.args.get(field, '')
            if value:
                filter[field] = value
        else:
            value = request.args.getlist(field)
            if len(value) > 1 and value[1].isdigit():
                if value[0] != 'no':
                    if value[0] == 'eq':
                        filter[field] = int(value[1])
                    elif value[0] == 'lt':
                        filter[field] = {'$lt': int(value[1])}
                    elif value[0] == 'gt':
                        filter[field] = {'$gt': int(value[1])}
    # to build the filter

    sample_list = mongo.db.samples.find(filter)
    sample_list_out =  list(mongo.db.samples.find(filter))

    for field in fields_string_type:
        string_field_element[field] = list(set(string_field_element[field]))
        string_field_element[field].sort()

    mapping = {}
    if language == 'cn':
        for field in all_fields_name:
            if mongo.db.mapping.find({'en': field}).count() > 0:
                mapping[field] = mongo.db.mapping.find({'en': field})[0]['cn']
            else:
                mapping[field] = field
    else:
        for field in all_fields_name:
            mapping[field] = field
    if language == 'en':
        posts = { # fake array of posts
            'Home': "Home",
            'Download':'Download',
            'Desp':'We need a description for every project.',
            'Projects': 'Projects',
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
            'OK':'OK',
            'star_pro':'Starred Projects',
            'new_pass':'New Password',
            'modify':'MODIFY',
            'S_F_F':'Set Fields Filter',
            'MORE':'MORE',
            'S_Fileds':'Select fields',
             'S_C':'Select Columns to Show',
             'Logout':'Logout',
            'profile':'Profile'
        }
    else:
        posts = { # fake array of posts
            'Home': U"主页",
            'Projects': U'工程',
            'Download':U'下载',

            'S_F_F':U'筛选文件设置',
            'MORE':U'更多',
            'S_Fileds':U'筛选范围',
            'S_C':U'按列筛选',
            'Desp':U'每个项目都需要描述',
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
            'OK':U'确认',
             'Logout':U'登出',
             'profile':U'个人简介'

        }
    all_fields_name.remove('name')
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        return render_template('samples.html', posts = posts,language=language, project_name=project_name,
                           sample_list=sample_list, project_fields_name=project_fields_name,
                           all_fields_name=all_fields_name, fields_string_type=fields_string_type,
                           string_field_element=string_field_element, mapping=mapping, user=user)
    return render_template('samples.html', posts = posts,language=language, project_name=project_name,
                           sample_list=sample_list, project_fields_name=project_fields_name,
                           all_fields_name=all_fields_name, fields_string_type=fields_string_type,
                           string_field_element=string_field_element, mapping=mapping)

