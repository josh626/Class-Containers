import json
from flask import Flask
from flask import render_template
from flaskext.markdown import Markdown
from modules import cc_get # as cc_get
app = Flask(__name__)
Markdown(app)
cc_projects = cc_get.get_projects()

@app.route('/')
def index():
    return render_template('homepage.html', cc_projects=cc_projects, value1="This is a Rendered Value!!!")


@app.route('/access/')
def access():
    return render_template('AccessCC.html', cc_projects=cc_projects)

@app.route('/dockerinfo/')
def dockerinfo():
    return render_template('dockerinfo.html', cc_projects=cc_projects)

@app.route('/containerimages/')
def containerimages():
    return render_template('Container_images.html', cc_projects=cc_projects)

@app.route('/howtousedocker/')
def howtousedocker():
    return render_template('HowToUseDocker.html', cc_projects=cc_projects)

@app.route('/launching/')
def launching():
    return render_template('L_S_Containers.html', cc_projects=cc_projects)

@app.route('/resources/')
def resources():
    return render_template('resources.html', cc_projects=cc_projects)

@app.route('/project/<project_id>')
def show_project(project_id):
    # TODO: add if for project_id empty --> route to '/'
    #       Render child template for list of projects (including any markdown) 
    #       assign rendered_project_child template to content 
    repos = cc_get.get_repos(project_id)

    project_id = int(project_id)
    project_list = cc_get.get_projects()
    project_data = {}
    for project in project_list:
        if project['project_id'] is project_id:
            project_data = project
    project_name = project_data['name']
    return render_template('class.html',
                           cc_projects=cc_projects,
                           cc_project_id=project_id,
                           cc_repos=repos,
                           cc_project_name=project_name,)

@app.route('/repo/<project_id>/<repo_id>')
def show_repo(project_id, repo_id):
    repo_id = int(repo_id)
    repo_list = cc_get.get_repos(project_id)
    repo_data = {}
    for repo in repo_list:
        if repo['id'] is repo_id:
            repo_data = repo

    repo_json_pretty = json.dumps(repo_data, sort_keys = True, indent = 4, separators = (',', ': '))
    repo_name = repo_data['name']
    repo_description = repo_data['description']
    repo_labels = repo_data['labels']
    repo_tags = cc_get.get_tags(repo_name)
    return render_template('repo.html',
                                   cc_projects=cc_projects,
                                   cc_repo_name=repo_name,
                                   cc_repo_description=repo_description,
                                   cc_repo_labels=repo_labels,
                                   cc_repo_id=repo_id,
                                   cc_repo_response=repo_json_pretty,
                                   cc_repo_tags=repo_tags
                                   )
    # TODO: add if for repo empty --> route to '/'
    #       Get label data
    #       Render child template using values from repo (markdown, Name, docker pull commands)
    #       assign rendered_repo_child template to content 

if __name__ == '__main__':
    app.run(host='0.0.0.0')
