import json
from flask import Flask
from flask import render_template
from flaskext.markdown import Markdown
from modules import cc_get # as cc_get
cc = Flask(__name__)
Markdown(cc)
cc_projects = cc_get.get_projects()

@cc.route('/')
def index():
    return render_template('homepage.html', cc_projects=cc_projects, value1="This is a Rendered Value!!!")

@cc.route('/project/<project_id>')
def show_project(project_id):
    # TODO: add if for project_id empty --> route to '/'
    #       Render child template for list of projects (including any markdown) 
    #       assign rendered_project_child template to content 
    repos = cc_get.get_repos(project_id)
    return render_template('class.html',
                           cc_projects=cc_projects,
                           cc_project_id=project_id,
                           cc_repos=repos)

@cc.route('/repo/<project_id>/<repo_id>')
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
    #       Generate docker pull commands
    #       Render child template using values from repo (markdown, Name, docker pull commands)
    #       assign rendered_repo_child template to content 

if __name__ == '__main__':
    cc.run(host='0.0.0.0')
