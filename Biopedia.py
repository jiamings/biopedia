# TODO: projects, profiles, data
from flask import Flask, render_template
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
    :return: The rendered index.html template.
    """
    return render_template('index.html', language=language)


@app.route('/projects')
@app.route('/<language>/projects')
def projects(language='en'):
    """
    Returns the projects page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered project.html template.
    """
    project_list = mongo.db.projects.find()
    return render_template('projects.html', language=language, project_list=project_list)


if __name__ == '__main__':
    app.run(debug=True)
