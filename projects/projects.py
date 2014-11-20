import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request, redirect, url_for
from models import User, StarredProjects, CreatedProjects
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
            created_project = CreatedProjects.objects(username=user['username'], project_name=project_name).count()
            if starred_project > 0:
                project['star'] = True
            else:
                project['star'] = False
            if created_project > 0:
                project['delete'] = True
            else:
                project['delete'] = False

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


@projects.route('/update-project',  methods=['GET'])
@projects.route('/<language>/update-project',  methods=['GET'])
def update_project_backend(language='en'):
    if 'username' in session:
        username = session['username']
        user = User.objects.get(username=username)
        project_name = request.args.get('projectname', '')
        count = CreatedProjects.objects(username=username, project_name=project_name).count()
        if count <= 0 and not user['admin']:
            return redirect(url_for('index.index_backend', language=language))
        else:
            mongo.db.samples.remove({'project_name': project_name})
            return redirect(url_for('.projects_backend', language=language))
    else:
        return redirect(url_for('index.index_backend', language=language))


@projects.route('/delete-project', methods=['GET'])
@projects.route('/<language>/delete-project', methods=['GET'])
def delete_project_backend(language='en'):

    file = request.files['update']
    mapping_file_secure_name = secure_filename(file.filename)

    if mapping_file_secure_name.split('.') <= 0 or mapping_file_secure_name.split('.')[-1] != 'json':
        return redirect(url_for('.projects_backend', language=language))
    
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
