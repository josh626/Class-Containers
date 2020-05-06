import json
import os
import requests
from flask import Flask, request, abort, redirect, Response, url_for, render_template
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flaskext.markdown import Markdown
from modules import cc_get # as cc_get
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = '33a0f3279e871573d885c9cf7ffbdaa2ca7ce3de2c86dfb8'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
Markdown(app)

host = "https://classcontainers.com:8444/api"


class User(UserMixin):

    def __init__(self, username, password, id, active=True):
        self.id = id 
        self.username = username
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

    def get_auth_token(self):
        return make_secure_token(self.username , key='secret_key')

    def get_id(self):
        return self.id


class UsersRepository:

    def __init__(self):
        self.users = dict()
        self.users_id_dict = dict()
        self.identifier = 0

    def save_user(self, user):
        self.users_id_dict.setdefault(user.id, user)
        self.users.setdefault(user.username, user)

    def get_user(self, username):
        return self.users.get(username)

    def get_user_by_id(self, userid):
        return self.users_id_dict.get(userid)

    def next_index(self):
        self.identifier +=1
        return self.identifier

users_repository = UsersRepository()


@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0],user_entry[1])
            if (user.password == password):
                return user
    return None


@login_manager.user_loader
def load_user(userid):
    return users_repository.get_user_by_id(userid)

@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        get = cc_get.Get(host, current_user.username, current_user.password) 
    else:
        return redirect(url_for('login'))
    return render_template('homepage.html', cc_projects=get.projects(), value1="This is a Rendered Value!!!")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login' , methods=['GET' , 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_validation = cc_get.Get(host, username, password).validate_user()
        if user_validation['status_code'] is 200:
            user_registered = users_repository.get_user(username)
            if user_registered == None:
                new_user = User(username , password , users_repository.next_index())
                users_repository.save_user(new_user)
                user_registered = users_repository.get_user(username)
                login_user(user_registered)
                return redirect(url_for('index'))
            else:
                login_user(user_registered)
                return redirect(url_for('index'))
        else:
             return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/access/')
def access():
    if current_user.is_authenticated:
        get = cc_get.Get(host, current_user.username, current_user.password) 
    else:
        return redirect(url_for('login'))
    return render_template('AccessCC.html', cc_projects=get.projects())

@app.route('/dockerinfo/')
def dockerinfo():
    if current_user.is_authenticated:
        get = cc_get.Get(host, current_user.username, current_user.password) 
    else:
        return redirect(url_for('login'))
    return render_template('dockerinfo.html', cc_projects=get.projects())

@app.route('/containerimages/')
def containerimages():
    if current_user.is_authenticated:
        get = cc_get.Get(host, current_user.username, current_user.password) 
    else:
        return redirect(url_for('login'))
    return render_template('Container_images.html', cc_projects=get.projects())

@app.route('/howtousedocker/')
def howtousedocker():
    if current_user.is_authenticated:
        get = cc_get.Get(host, current_user.username, current_user.password) 
    else:
        return redirect(url_for('login'))
    return render_template('HowToUseDocker.html', cc_projects=get.projects())

@app.route('/launching/')
def launching():
    if current_user.is_authenticated:
        get = cc_get.Get(host, current_user.username, current_user.password) 
    else:
        return redirect(url_for('login'))
    return render_template('L_S_Containers.html', cc_projects=get.projects())

@app.route('/resources/')
def resources():
    if current_user.is_authenticated:
        get = cc_get.Get(host, current_user.username, current_user.password) 
    else:
        return redirect(url_for('login'))
    return render_template('resources.html', cc_projects=get.projects())

@app.route('/register' , methods=['GET' , 'POST'])
def register():
    # Pass-through user registration to Harbor
    if request.method == 'POST':
        print("REGISTER POST!!!")
        print("request: {}".format(request))
        print("request.form: {}".format(request.form))
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password-repeat']
        realname = request.form['realname']
        email = request.form['email']
        print("username: {}".format(username))
        if password != password_repeat:
            return redirect(url_for('register'))
        host = "https://classcontainers.com:8444/api/users"
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        body = {"username": username, "password": password, "realname": realname, "email": email, "comment": ""}
        try:
            raw_response = requests.post(host, headers=headers, json=body)
            print("raw_response: {}".format(raw_response))
            print("    status_code: {}".format(raw_response.status_code))
            print("    json: {}".format(raw_response.json()))
            if raw_response.status_code not in (200, 201):
                return redirect(url_for('register'))
            return redirect(url_for('login'))
        except Exception as e:
            print("Failure submitting user registration: {}".format(e))
            print("raw_response: {}".format(raw_response))
            print("    status_code: {}".format(raw_response.status_code))
            return redirect(url_for('login'))
    else:
        return render_template('register.html')


    

@app.route('/project/<project_id>')
@login_required
def show_project(project_id):
    # TODO: add if for project_id empty --> route to '/'
    if current_user.is_authenticated:
        get = cc_get.Get(host, current_user.username, current_user.password) 
    else:
        return redirect(url_for('login'))
    repos = get.repos(project_id)
    project_id = int(project_id)
    project_list = get.projects()
    project_data = {}
    for project in project_list:
        if project['project_id'] is project_id:
            project_data = project
    project_name = project_data['name']
    return render_template('class.html',
                           cc_projects=get.projects(),
                           cc_project_id=project_id,
                           cc_repos=repos,
                           cc_project_name=project_name,)

@app.route('/repo/<project_id>/<repo_id>')
@login_required
def show_repo(project_id, repo_id):
    if current_user.is_authenticated:
        get = cc_get.Get(host, current_user.username, current_user.password) 
    else:
        return redirect(url_for('login'))
    repo_id = int(repo_id)
    repo_list = get.repos(project_id)
    repo_data = {}
    for repo in repo_list:
        if repo['id'] is repo_id:
            repo_data = repo

    repo_json_pretty = json.dumps(repo_data, sort_keys = True, indent = 4, separators = (',', ': '))
    repo_name = repo_data['name']
    repo_description = repo_data['description']
    repo_labels = repo_data['labels']
    repo_tags = get.tags(repo_name)
    return render_template('repo.html',
                                   cc_projects=get.projects(),
                                   cc_repo_name=repo_name,
                                   cc_repo_description=repo_description,
                                   cc_repo_labels=repo_labels,
                                   cc_repo_id=repo_id,
                                   cc_repo_response=repo_json_pretty,
                                   cc_repo_tags=repo_tags
                                   )

if __name__ == '__main__':
    app.run(host='0.0.0.0')
