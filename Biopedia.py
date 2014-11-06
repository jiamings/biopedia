"""
Main Entrance for the application.
"""
from flask import Flask, render_template, request, redirect, url_for, escape, session
from flask.ext.pymongo import PyMongo

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
        user = mongo.db.testData.find_one({"username": session['username']})
        return render_template('index.html', language=language, username=session['username'],
                               firstname=user['firstname'], lastname=user['lastname'])
    return render_template('index.html', language=language)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # whether we find the target username in the database or not
    user = mongo.db.testData.find_one({"username": username})

    if user:
        if user["password"] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index', alert_place="register", alert_message="Password incorrect."))
    else:
        return redirect(url_for('index', alert_place="register", alert_message="User does not exist."))


@app.route('/register', methods=['POST'])
def register():
    # login information
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    user = mongo.db.testData.find_one({"username": username})
    if user:
        return redirect(url_for('index', alert_place="register", alert_message="Username has been registered."))

    user = mongo.db.testData.find_one({"email": email})
    if user:
        return redirect(url_for('index', alert_place="register", alert_message="Email has been registered."))

    user = {
        "username": username,
        "password": password,
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
    }

    mongo.db.testData.insert(user)

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
        project_fields_name = default_selected_fields[project_name]
    # to take the keys of one of the sample as heads of the sample table
    all_fields_name = dict(sample_list[0]).keys()
    all_fields_name.remove("_id")
    all_fields_name.remove("project_name")
    all_fields_name.sort()
    # get all the fields (for more fields)
    fields_string_type = default_fields_string_type[project_name]
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
            if mongo.db.mapping.find({'en': field}).count() > 0:
                mapping[field] = mongo.db.mapping.find({'en': field})[0]['cn']
            else:
                mapping[field] = field
    else:
        for field in all_fields_name:
            mapping[field] = field

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
    return render_template('profile.html', language=language, sample_name=sample_name,
                           project_name=project_name, sample_detail=sample_detail,
                           selected_details_name=selected_details)

@app.route('/user', methods=['GET'])
@app.route('/<language>/profile', methods=['GET'])
def profile(language='en'):
    if session['username']:
        username = session['username']
        user = mongo.db.testData.find_one({"username": username})
        firstname = user['firstname']
        lastname = user['lastname']
        email = user['email']
        return render_template('user.html', username=username, firstname=firstname, lastname=lastname, email=email, language=language)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
