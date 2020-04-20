import requests
import json
from base64 import b64encode
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

uname_pass = b64encode(b"admin:Harbor12345").decode("ascii")
headers = {'Authorization' : 'Basic {}'.format(uname_pass)}

def get_projects():
    try:
        response = requests.get("https://srv-harbor-00.tomchris.net/api/projects", headers=headers, verify=False)
        return response.json()

    except Exception as except_err:
        print("Failed obtaining list of projects: {}".format(except_err))


def get_repos(project_id):
    try:
        response = requests.get("https://srv-harbor-00.tomchris.net/api/repositories?project_id={}".format(project_id), headers=headers, verify=False)
        return response.json()

    except Exception as except_err:
        print("Failed obtaining list of repositories: {}".format(except_err))

def get_resource(resource):
    try:
        response = requests.get("https://srv-harbor-00.tomchris.net/api/{}".format(resource), headers=headers, verify=False)
        return response.json()

    except Exception as except_err:
        print("Failed obtaining list of {}: {}".format(resource, except_err))

def get_users():
    try:
        response = requests.get("https://srv-harbor-00.tomchris.net/api/users", headers=headers, verify=False)
        return response.json()

    except Exception as except_err:
        print("Failed obtaining list of users: {}".format(except_err))
