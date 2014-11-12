import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request
from models import User, StarredProjects
from definition import mongo

projects = Blueprint('projects', __name__, template_folder='templates')

@projects.route('/projects', methods=['GET'])
@projects.route('/<language>/projects', methods=['GET'])
def projects_backend(language='en'):
    """
    Returns the projects page.
    :param language: Defines the language ('en' or 'cn') used for the template.
    :return: The rendered project.html template which contains all the projects for now.
                /projects
    """
    project_list = list(mongo.db.projects.find())
    if 'username' in session:
        user = User.objects.get(username=session['username'])
        for project in project_list:
            project_name = project['name']
            starred_project = StarredProjects.objects(username=user['username'], project_name=project_name).count()
            if starred_project > 0:
                project['star'] = True
            else:
                project['star'] = False

        return render_template('projects.html', language=language, project_list=project_list, user=user)
    return render_template('projects.html', language=language, project_list=project_list)
