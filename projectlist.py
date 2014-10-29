import pymongo
from datetime import date

client = pymongo.MongoClient()


def save_project(name, environment, site, sequence_type,
                 project_id, num_of_total_sequences,
                 num_of_orfs, num_of_samples, read_length,
                 platform, create_date, update_date):
    """
    Insert a project into the "projects" database, with the following parameters specified.
    :param name:
    :param environment:
    :param site:
    :param sequence_type:
    :param project_id:
    :param num_of_total_sequences:
    :param num_of_orfs:
    :param num_of_samples:
    :param read_length:
    :param platform:
    :param create_date:
    :param update_date:
    :return: True if insertion is successful, and False otherwise.
    """
    db = client.Biopedia

    if type(name) != str:
        return False
    elif type(environment) != str:
        return False
    elif type(site) != str:
        return False
    elif type(sequence_type) != str:
        return False
    elif type(project_id) != str:
        return False
    elif type(num_of_total_sequences) != int:
        return False
    elif type(num_of_orfs) != int:
        return False
    elif type(num_of_samples) != int:
        return False
    elif type(read_length) != int:
        return False
    elif type(platform) != str:
        return False
    elif type(create_date) != dict:
        return False
    elif type(update_date) != dict:
        return False

    same_project = db.projects.find({"project_id": project_id})
    if same_project.count() != 0:
        return False

    proj_info = {
        "name": name,
        "environment": environment,
        "site": site,
        "sequence_type": sequence_type,
        "project_id": project_id,
        "num_of_total_sequences": num_of_total_sequences,
        "num_of_orfs": num_of_orfs,
        "num_of_samples": num_of_samples,
        "read_length": read_length,
        "platform": platform,
        "create_date": create_date,
        "update_date": update_date,
    }
    db.projects.save(proj_info)
    return True
