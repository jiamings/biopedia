import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request
from models import User, StarredProjects
from definition import mongo
import os
from werkzeug.utils import secure_filename


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

        os.system("rm -f %s" % mapping_file_secure_name)
        os.system("rm -f %s" % samples_file_secure_name)

    if mongo.db.samples.count({"project_name": name})>0:
        samples = mongo.db.samples.find({"project_name": name})
        fields = samples[0].keys()
        fields.remove("project_name")
        fields.remove("_id")
        string_fields = []
        default_fields = []
        for field in fields:
            # check if string
            for sample in samples:
                if sample[field] != 'NA' and not sample[field].isdigit():
                    string_fields.insert(field)
                    break
            # create default
            if field in default_default_fields:
                default_fields.insert(field)
        mongo.db.fields.insert({"project_name": name, "default_fields": default_fields,
                                "string_fields": string_fields})

    project_list = mongo.db.projects.find()

    if 'username' in session:
        user = User.objects.get(username=session['username'])

    if 'username' in session:
        return render_template('projects.html', language=language, project_list=project_list, user=user)
    else:
        return render_template('projects.html', language=language, project_list=project_list)
