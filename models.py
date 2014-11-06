from mongoengine import *

connect('Biopedia')

class User(Document):
    username = StringField(required=True, max_length=16)
    admin = BooleanField(required=True)
    email = StringField(required=True)
    firstname = StringField(required=True, max_length=50)
    lastname = StringField(required=True, max_length=50)
    password = StringField(required=True, max_length=50)


class StarredProjects(Document):
    username = StringField(required=True, max_length=16)
    project_name = StringField(required=True)