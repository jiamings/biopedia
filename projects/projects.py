#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request, redirect, url_for
from models import User, StarredProjects, CreatedProjects
from definition import mongo
import os
from werkzeug.utils import secure_filename


projects = Blueprint('projects', __name__, template_folder='templates')

@projects.route('/<language>/projects', methods=['GET'])
def projects_backend(language):
    """
    Returns the projects page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered project.html template which contains all the projects for now.
                /projects
    """
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
            'proj_comment':'Create your own project!',
            'Insert_pro':'Register a free account to create your own project!',
            'Environment':'Environment',
            'Site':'Site',
            'seq_type':'Sequence Type',
            'pro_id':'Project Id',
            'F':'# of Total Sequences',
            'S':'# of ORFs',
            'T':'# of Samples',
            'Fo':'Read Length',
            'Fi':'Platform',
            'Si':'Create Date',
            'Se':'Update Date',
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
            'cannot_be_revert':'This operation cannot be reverted.',
            'NO':'No',
            'Yes':'Yes',
            'insert_N':'Insert a new PROJECT!',
            'Name':'Name',
            'Logout':'Logout',
            'profile':'Profile'
        }
    else:
        posts = { # fake array of posts
            'Home': U"主页",
            'Projects': U'工程',
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
            'proj_comment':U'添加你自己的项目',
            'Insert_pro':U'注册一个免费的账号来添加自己的项目',
            'Environment':U'环境',
            'Site':U'地域',
            'seq_type':U'结论类型',
            'pro_id':U'项目编号',
            'F':U'# 全序列',
            'S':U'# 开关频谱',
            'T':U'# 样本数',
            'Fo':U'读入长度',
            'Fi':U'平台',
            'Si':U'创建时间',
            'Se':U'更新时间',
            'Star':U'赞',
            'Delete':U'删除',
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
            'cannot_be_revert':U'操作不可被恢复',
            'NO':U'否',
            'Yes':U'是',
            'insert_N':U'添加一个新项目',
             'Name':U'名称',
              'Logout':U'登出',
             'profile':U'个人简介'
        }
    project_list = list(mongo.db.projects.find())
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        for project in project_list:
            project_name = project['name']
            starred_project = StarredProjects.objects(username=user['username'], project_name=project_name).count()
            created_project = CreatedProjects.objects(username=user['username'], project_name=project_name).count()
            if starred_project > 0:
                project['star'] = True
            else:
                project['star'] = False
            if created_project > 0:
                project['delete'] = True
            else:
                project['delete'] = False

        return render_template('projects.html', posts = posts,language=language, project_list=project_list, user=user)
    return render_template('projects.html', posts = posts,language=language, project_list=project_list)


default_default_fields = {"sex", "age", "residence", "Nationality",
                    "married", "drink", "smoke"}

UPLOAD_FOLDER = '.'

@projects.route('/projects_insert', methods=['POST'])
@projects.route('/<language>/projects_insert', methods=['POST'])
def projects_insert(language='en'):
    """

    :param language:
    :return:
    """
    name = request.form['name']
    environment = request.form['environment']
    site = request.form['site']
    sequence_type = request.form['sequence_type']
    project_id = request.form['project_id']
    num_of_total_sequences = request.form['num_of_total_sequences']
    num_of_orfs = request.form['num_of_orfs']
    num_of_samples = request.form['num_of_samples']
    read_length = request.form['read_length']
    platform = request.form['platform']
    create_date = request.form['create_date']
    update_date = request.form['update_date']

    mapping_file = request.files['mapping']
    mapping_file_secure_name = secure_filename(mapping_file.filename)

    samples_file = request.files['samples']
    samples_file_secure_name = secure_filename(samples_file.filename)

    succeed = str(name) and mongo.db.projects.find({'name': name}).count() == 0

    succeed = succeed and environment and site and sequence_type and project_id and \
              str(num_of_total_sequences).isdigit() and str(num_of_orfs).isdigit() and \
              str(read_length).isdigit() and platform

    if len(str(create_date).split('/'))==3 and str(create_date).split('/')[0].isdigit() and \
            str(create_date).split('/')[1].isdigit() and str(create_date).split('/')[2].isdigit():
        create_date = {'month': int(str(create_date).split('/')[0]),
                       'day': int(str(create_date).split('/')[1]),
                       'year': int(str(create_date).split('/')[2]) }
    else:
        succeed = False

    if len(str(update_date).split('/'))==3 and str(update_date).split('/')[0].isdigit() and \
            str(update_date).split('/')[1].isdigit() and str(update_date).split('/')[2].isdigit():
        update_date = {'month': int(str(update_date).split('/')[0]),
                       'day': int(str(update_date).split('/')[1]),
                       'year': int(str(update_date).split('/')[2]) }
    else:
        succeed = False

    if len(mapping_file_secure_name.split('.')) <=0 or mapping_file_secure_name.split('.')[-1] != 'csv'  or \
            len(samples_file_secure_name.split('.')) <= 0 or samples_file_secure_name.split('.')[-1] != 'json':
        succeed = False
    else:
        fvalue = mapping_file.read()
        mapping_file.seek(0)
        mapping_file.save(os.path.join(UPLOAD_FOLDER, mapping_file_secure_name))

        fvalue = samples_file.read()
        samples_file.seek(0)
        samples_file.save(os.path.join(UPLOAD_FOLDER, samples_file_secure_name))

    if succeed:
        proj_info = {
            "name": name,
            "environment": environment,
            "site": site,
            "sequence_type": sequence_type,
            "project_id": project_id,
            "num_of_total_sequences": int(num_of_total_sequences),
            "num_of_orfs": int(num_of_orfs),
            "num_of_samples": int(num_of_samples),
            "read_length": read_length,
            "platform": platform,
            "create_date": create_date,
            "update_date": update_date,
        }
        mongo.db.projects.save(proj_info)

        os.system("mongoimport -c mapping -d Biopedia --file %s --type csv --headerline" % mapping_file_secure_name)
        os.system("mongoimport -c samples -d Biopedia --file %s" % samples_file_secure_name)

        os.system("rm -f %s" % mapping_file_secure_name)
        os.system("rm -f %s" % samples_file_secure_name)

    if mongo.db.samples.find({"project_name": name}).count() > 0:
        samples = mongo.db.samples.find({"project_name": name})
        fields = samples[0].keys()
        fields.remove("project_name")
        fields.remove("_id")
        string_fields = []
        default_fields = []
        for field in fields:
            # check if string
            samples = mongo.db.samples.find({"project_name": name})

            for sample in samples:
                if sample[field] != 'NA' and type(sample[field])!=int:
                    string_fields.append(field)
                    break
            # create default
            if field in default_default_fields:
                default_fields.append(field)
        mongo.db.fields.insert({"project_name": name, "default_fields": default_fields,
                                "string_fields": string_fields})
        user = User.objects.get(username=session['username'])
        project_name = name
        created_project = CreatedProjects(username=user['username'], project_name=project_name)
        created_project.save()

    project_list = mongo.db.projects.find()

    if 'username' in session:
        user = User.objects.get(username=session['username'])

    return redirect(url_for('projects.projects_backend', language=language))


@projects.route('/update-project',  methods=['POST'])
@projects.route('/<language>/update-project',  methods=['POST'])
def update_project_backend(language='en'):
    file = request.files['update']
    file_secure_name = secure_filename(file.filename)

    project_name = request.form['project_name']

    if file_secure_name.split('.') <= 0 or file_secure_name.split('.')[-1] != 'json':
        if project_name:
            return redirect(url_for('samples.samples_backend', language=language, project_name=project_name))
        else:
            return redirect(url_for('.projects_backend', language=language))

    file.seek(0)
    file.save(os.path.join(UPLOAD_FOLDER, file_secure_name))

    if 'username' in session:
        username = session['username']
        user = User.objects.get(username=username)
        count = CreatedProjects.objects(username=username, project_name=project_name).count()
        if count <= 0 and not user['admin']:
            return redirect(url_for('index.index_backend', language=language))
        else:
            mongo.db.samples.remove({'project_name': project_name})
            os.system("mongoimport -c samples -d Biopedia --file %s" % file_secure_name)
            os.system("rm -f %s" % file_secure_name)
            return redirect(url_for('samples.samples_backend', language=language, name=project_name))
    else:
        return redirect(url_for('index.index_backend', language=language))


@projects.route('/delete-project', methods=['GET'])
@projects.route('/<language>/delete-project', methods=['GET'])
def delete_project_backend(language='en'):

    if 'username' in session:
        username = session['username']
        user = User.objects.get(username=username)
        project_name = request.args.get('projectname', '')
        count = CreatedProjects.objects(username=username, project_name=project_name).count()
        if count <= 0 and not user['admin']:
            return redirect(url_for('index.index_backend', language=language))
        else:
            CreatedProjects.objects(project_name=project_name).delete()
            StarredProjects.objects(project_name=project_name).delete()
            mongo.db.projects.remove({'name': project_name})
            mongo.db.samples.remove({'project_name': project_name})
            mongo.db.fields.remove({'project_name': project_name})
            mongo.db.mapping.remove({'project_name': project_name})
            return redirect(url_for('.projects_backend', language=language))
    else:
        return redirect(url_for('index.index_backend', language=language))
