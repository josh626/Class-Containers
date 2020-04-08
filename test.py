from modules import cc_get # as cc_get
import json

print("users: {}".format(json.dumps(cc_get.get_users(), indent=2)))

print("projects: {}".format(json.dumps(cc_get.get_projects(), indent=2)))
