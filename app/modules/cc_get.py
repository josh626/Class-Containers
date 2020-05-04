import requests
import json
from base64 import b64encode
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Get:
    """ Get Methods. 
        Usage: get = cc_get.Get(host, uname, password)
               get.projects()
        returns response.json()
    """
    def __init__(self, host, uname, password):
        self.host = host
        uname_pass = "{}:{}".format(uname, password)
        if type(uname_pass) == str:
            self.headers = {'Authorization' : 'Basic {}'.format(b64encode(uname_pass.encode('utf-8')).decode("ascii"))}
        else:
            self.headers = {'Authorization' : 'Basic {}'.format(b64encode(uname_pass).decode("ascii"))}


    def resource(self, resource):
        try:
            raw_response = requests.get("{}/{}".format(self.host, resource),
                                    headers=self.headers, verify=False)
            response = {
                    "status_code": raw_response.status_code,
                    "headers": raw_response.headers,
                    "json": raw_response.json()}
            return response

        except Exception as except_err:
            print("Failed requesting {}: {}".format(resource, except_err))

    def validate_user(self):
        try:
            response = self.resource("/users/current")
            return response
        except Exception as except_err:
            print("Failure Validating User: {}".format(except_err))
    
    def projects(self):
        try:
            response = self.resource("/projects")
            return response['json']

        except Exception as except_err:
            print("Failed obtaining list of projects: {}".format(except_err))


    def repos(self, project_id):
        try:
            response = self.resource("/repositories?project_id={}".format(project_id))
            return response['json']

        except Exception as except_err:
            print("Failed obtaining list of repositories: {}".format(except_err))

    def tags(self, repo_name):
        try:
            response = self.resource("/repositories/{}/tags".format(repo_name))
            tags = []
            for tag in response['json']:
                tags.append(tag['name'])
            return tags 

        except Exception as except_err:
            print("Failed obtaining list of repositories: {}".format(except_err))

    def users(self):
        try:
            response = self.resource("/users")
            return response['json']

        except Exception as except_err:
            print("Failed obtaining list of users: {}".format(except_err))
