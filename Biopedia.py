"""
Main Entrance for the application.
"""
from flask import Flask, render_template, request, redirect, url_for, escape, session
from flask.ext.pymongo import PyMongo


app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
@app.route('/<language>/index')
def index(language='en'):
    """
    Returns the index page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered index.html template, which currently contains almost nothing.
    """
    return render_template('index.html', language=language)


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
    {"MetaTongue": ["sex", "age", "residence", "Nationality", "married", "drink", "smoke", "tongueColor", "tongueType"]}

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
    # the project_name ought to be exist in db projects
    assert mongo.db.samples.find({"project_name": project_name}).count() > 0
    # the project_name ought to be exist in db samples
    sample_list = mongo.db.samples.find({"project_name": project_name})
    #project_fields_name = dict(sample_list[0]).keys()
    #project_fields_name.remove("_id")
    #project_fields_name.remove("project_name")
    if request.args.get("fields",''):
        project_fields_name = request.args.getlist("fields")
        print(project_fields_name)
    else:
        project_fields_name = default_selected_fields[project_name]
    if len(project_fields_name) > 10:
        project_fields_name = project_fields_name[0:9]
    # to take the keys of one of the sample as heads of the sample table
    all_fields_name = dict(sample_list[0]).keys()
    all_fields_name.remove("_id")
    all_fields_name.remove("project_name")
    all_fields_name.sort()
    return render_template('samples.html', language=language, project_name=project_name,
                           sample_list=sample_list, project_fields_name=project_fields_name,
                           all_fields_name=all_fields_name)

@app.route('/charts', methods=['GET'])
def charts():
    return render_template('charts.html')


default_selected_details = \
    {"MetaTongue":["name", "sex", "age", "residence", "Nationality",
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
    assert mongo.db.samples.find({"name": sample_name, "project_name": project_name}).count() > 0
    # get sample name and project name from REQUEST
    sample_detail = mongo.db.samples.find({"name": sample_name, "project_name": project_name})[0]
    selected_details = default_selected_details[project_name]
    # select certain details
    return render_template('profile.html', language=language, sample_name=sample_name,
                           project_name=project_name, sample_detail=sample_detail,
                           selected_details_name=selected_details)

if __name__ == '__main__':
    app.run(debug=True)
