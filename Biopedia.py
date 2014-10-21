"""
Main Entrance for the application.
"""
from flask import Flask, render_template, request
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
    assert mongo.db.projects.find({"name":project_name}).count() > 0
    # the project_name ought to be exist in db projects
    assert mongo.db.samples.find({"project_name":project_name}).count() > 0
    # the project_name ought to be exist in db samples
    sample_list = mongo.db.samples.find({"project_name":project_name})
    project_fields_name = dict(sample_list[0])['elements'].keys()
    # to take the keys of one of the sample as heads of the sample table
    # a sample consists 'project_name it belongs to' and 'elements' dict
    return render_template('samples.html', language=language,
                           sample_list=sample_list, project_fields_name=project_fields_name)


if __name__ == '__main__':
    app.run(debug=True)
