"""
Main Entrance for the application.
"""
from index.index import index
from projects.projects import projects
from projects.samples import samples
from projects.profile import sample_profile
from user.login import user_login
from user.profile import user_profile
from user.admin import user_admin
from workflow.workflow import workflow_bp
from definition import app

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.register_blueprint(index)
app.register_blueprint(projects)
app.register_blueprint(samples)
app.register_blueprint(user_login)
app.register_blueprint(user_profile)
app.register_blueprint(sample_profile)
app.register_blueprint(user_admin)
app.register_blueprint(workflow_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
