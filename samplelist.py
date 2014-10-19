__author__ = 'yuanyuan'

import pymongo

client = pymongo.MongoClient()

def save_sample(project_name, elements):
    """
    :param project_name: name of the sample belongs to
    :param elements: all the info of the sample, saved as an array
    :return: True if insertion is successful, and False otherwise.
    """

    db = client.Biopedia

    if (type(elements)!=dict):
        return False

    if db.projects.find({'name':project_name}).count()==0:
        return False

    if db.samples.find().count()>0 and len(db.samples.find().limit(1)[0]['elements'])<>len(elements):
        return False

    samp_info = {
        "project_name": project_name,
        "elements": elements,
    }
    db.samples.save(samp_info)
    return True
