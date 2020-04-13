import json
from flask import Flask
from flask import render_template
from modules import cc_get # as cc_get
cc = Flask(__name__)

cc_projects = cc_get.get_projects()

@cc.route('/')
def index():
    return render_template('index.html', cc_projects=cc_projects, value1="This is a Rendered Value!!!")

@cc.route('/project/<project_id>')
def show_project(project_id):
    print("project_id: {}".format(project_id))
    # TODO: add if for project_id empty --> route to '/'
    repos = cc_get.get_repos(project_id)
    return render_template('class.html', cc_projects=cc_projects, cc_project_id=project_id, cc_repos=repos)

@cc.route('/repo/<repo_id>')
def show_repo(repo_id):
    # TODO: add if for project_id empty --> route to '/'
    return render_template('repo.html', cc_projects=cc_projects, cc_repo_id=repo_id)

if __name__ == '__main__':
    cc.run(host='0.0.0.0')
