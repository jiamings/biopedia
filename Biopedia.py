"""
Main Entrance for the application.
"""
from flask import Flask, render_template, request, redirect, url_for, escape, session
from flask.ext.pymongo import PyMongo
from models import *
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
mongo = PyMongo(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
@app.route('/index')
@app.route('/<language>/index')
def index(language='en'):
    """
    Returns the index page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered index.html template, which currently contains almost nothing.
    """
    alert_place = request.args.get('alert_place', '')
    alert_message = request.args.get('alert_message', '')
    if alert_message and alert_place:
        return render_template('index.html', language=language, alert_place=alert_place, alert_message=alert_message)
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        return render_template('index.html', language=language, user=user)
    return render_template('index.html', language=language)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # whether we find the target username in the database or not
    user = User.objects.get(username=username)
    if user:
        if user["password"] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index', alert_place="login", alert_message="Password incorrect."))
    else:
        return redirect(url_for('index', alert_place="login", alert_message="User does not exist."))


@app.route('/register', methods=['POST'])
def register():
    # login information
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    num_users = User.objects(username=username).count()
    if num_users > 0:
        return redirect(url_for('index', alert_place="register", alert_message="Username has been registered."))

    num_users = User.objects(email=email).count()
    if num_users > 0:
        return redirect(url_for('index', alert_place="register", alert_message="Email has been registered."))

    user = User(username=username,
                password=password,
                email=email,
                firstname=firstname,
                lastname=lastname,
                admin=False)

    user.save()

    session['username'] = username
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/projects', methods=['GET'])
@app.route('/<language>/projects', methods=['GET'])
def projects(language='en'):
    """
    Returns the projects page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered project.html template which contains all the projects for now.
                /projects
    """
    project_list = mongo.db.projects.find()
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        return render_template('projects.html', language=language, project_list=project_list, user=user)
    return render_template('projects.html', language=language, project_list=project_list)

UPLOAD_FOLDER = '.'

@app.route('/projects_insert', methods=['POST'])
@app.route('/<language>/projects_insert', methods=['POST'])
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

    print 'name'
    print name
    mapping_file = request.files['mapping']
    mapping_file_secure_name = secure_filename(mapping_file.filename)

    samples_file = request.files['samples']
    samples_file_secure_name = secure_filename(samples_file.filename)

    print(mapping_file_secure_name)
    print(samples_file_secure_name)

    succeed = str(name) and mongo.db.projects.find({'name': name}).count() == 0

    print succeed

    succeed = succeed and environment and site and sequence_type and project_id and \
              str(num_of_total_sequences).isdigit() and str(num_of_orfs).isdigit() and \
              str(read_length).isdigit() and platform

    print succeed

    if len(str(create_date).split('/'))==3 and str(create_date).split('/')[0].isdigit() and \
            str(create_date).split('/')[1].isdigit() and str(create_date).split('/')[2].isdigit():
        create_date = {'month': int(str(create_date).split('/')[0]),
                       'day': int(str(create_date).split('/')[1]),
                       'year': int(str(create_date).split('/')[2]) }
    else:
        succeed = False

    print succeed

    if len(str(update_date).split('/'))==3 and str(update_date).split('/')[0].isdigit() and \
            str(update_date).split('/')[1].isdigit() and str(update_date).split('/')[2].isdigit():
        update_date = {'month': int(str(update_date).split('/')[0]),
                       'day': int(str(update_date).split('/')[1]),
                       'year': int(str(update_date).split('/')[2]) }
    else:
        succeed = False

    print succeed

    if mapping_file_secure_name.split('.')[-1] != 'csv' or samples_file_secure_name.split('.')[-1] != 'json':
        succeed = False
    else:
        fvalue = mapping_file.read()
        #vs = str(fvalue).split('\\r\\n')
        #fvalue = 'project_name,en,cn,details'
        #for v in vs:
        #    fvalue += name + ',' + v + '\r\n'
       # print fvalue
        mapping_file.seek(0)
        mapping_file.save(os.path.join(UPLOAD_FOLDER, mapping_file_secure_name))

        fvalue = samples_file.read()
        samples_file.seek(0)
        samples_file.save(os.path.join(UPLOAD_FOLDER, samples_file_secure_name))

    print succeed

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

        os.system("del %s" % mapping_file_secure_name)
        os.system("del %s" % samples_file_secure_name)

    project_list = mongo.db.projects.find()

    if 'username' in session:
        user = User.objects.get(username=session['username'])

    if 'username' in session:
        return render_template('projects.html', language=language, project_list=project_list, user=user)
    else:
        return render_template('projects.html', language=language, project_list=project_list)


default_selected_fields = \
    {"MetaTongue": ["sex", "age", "residence", "Nationality",
                    "married", "drink", "smoke", "tongueColor", "tongueType"]}

default_fields_string_type = {
    "MetaTongue": ["sex", "residence", "Nationality", "tongueColor"]}


@app.route('/samples', methods=['GET'])
@app.route('/<language>/samples', methods=['GET'])
def samples(language='en'):
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

    for field in fields_string_type:
        string_field_element[field] = list(set(string_field_element[field]))
        string_field_element[field].sort()

    mapping = {}
    if language == 'cn':
        for field in all_fields_name:
            if mongo.db.mapping.find({'project_name': project_name, 'en': field}).count() > 0:
                mapping[field] = mongo.db.mapping.find({'project_name': project_name, 'en': field})[0]['cn']
            else:
                mapping[field] = field
    else:
        for field in all_fields_name:
            mapping[field] = field

    all_fields_name.remove('name')
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        return render_template('samples.html', language=language, project_name=project_name,
                           sample_list=sample_list, project_fields_name=project_fields_name,
                           all_fields_name=all_fields_name, fields_string_type=fields_string_type,
                           string_field_element=string_field_element, mapping=mapping, user=user)
    return render_template('samples.html', language=language, project_name=project_name,
                           sample_list=sample_list, project_fields_name=project_fields_name,
                           all_fields_name=all_fields_name, fields_string_type=fields_string_type,
                           string_field_element=string_field_element, mapping=mapping)


default_selected_details = \
    {"MetaTongue": ["name", "sex", "age", "residence", "Nationality",
                    "married", "drink", "smoke"]}


@app.route('/profile', methods=['GET'])
@app.route('/<language>/profile', methods=['GET'])
def sample_profile(language='en'):
    """

    :param language: language: Defines the language ('en' or 'cn') used for the template
    :return: The rendered samples.html template
              /samples?project=<project_name>&name=<sample_name>
    """
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
        return render_template('profile.html', language=language, sample_name=sample_name,
                        project_name=project_name, sample_detail=sample_detail,
                        selected_details_name=selected_details, user=user)
    return render_template('profile.html', language=language, sample_name=sample_name,
                           project_name=project_name, sample_detail=sample_detail,
                           selected_details_name=selected_details)


@app.route('/user', methods=['GET'])
@app.route('/<language>/user', methods=['GET'])
def profile(language='en'):
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
        return redirect(url_for('index'))

@app.route('/user-admin')
@app.route('/<language>/user-admin')
def user_admin(language='en'):
    if session['username']:
        username = session['username']
        user = User.objects.get(username=username)
        if not user['admin']:
            return redirect(url_for('index'))
        else:
            firstname = user['firstname']
            lastname = user['lastname']
            email = user['email']
            users_list = User.objects()
            return render_template('user-admin.html', firstname=firstname, lastname=lastname,
                                   email=email, language=language, users_list=users_list)
    else:
        return redirect(url_for('index'))


@app.route('/delete-user')
def delete_user():
    username = request.args.get('username', '')
    user = User.objects.get(username=username)
    if user:
        user.delete()
    return redirect(url_for('user_admin'))


@app.route('/modify-password', methods=['POST'])
def modify_password():
    password = request.form['originalPassword']
    newpassword = request.form['newPassword']
    username = session['username']
    user = User.objects.get(username=username)
    if user['password'] == password:
        User.objects(id=user.id).update_one(set__password=newpassword)
        return redirect(url_for('profile', alert_type="alert-success", alert_message="Successfully changed password!"))
    else:
        return redirect(url_for('profile', alert_type="alert-danger", alert_message="Password incorrect."))


if __name__ == '__main__':
    app.run(debug=True)
