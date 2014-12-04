#!/usr/bin/python
#-*-coding:utf-8-*-
import sys
sys.path.append('../')

from flask import Blueprint, render_template, session, request, redirect, url_for
from models import User
from definition import mongo

sample_profile = Blueprint('sample_profile', __name__, template_folder='templates')

default_selected_details = \
    {"MetaTongue": ["name", "sex", "age", "residence", "Nationality",
                    "married", "drink", "smoke"]}

@sample_profile.route('/profile', methods=['GET'])
@sample_profile.route('/<language>/profile', methods=['GET'])
def profile_backend(language='en'):
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
        return render_template('profile.html',language=language, sample_name=sample_name,
                        project_name=project_name, sample_detail=sample_detail,
                        selected_details_name=selected_details, user=user)
    return render_template('profile.html',language=language, sample_name=sample_name,
                           project_name=project_name, sample_detail=sample_detail,
                           selected_details_name=selected_details)
