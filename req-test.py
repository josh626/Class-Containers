import requests
import json
from base64 import b64encode
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


uname_pass = b64encode(b"admin:Harbor12345").decode("ascii")
headers = {'Authorization' : 'Basic {}'.format(uname_pass)}
#response = requests.get("https://classcontainers.com/api/v2.0/users", headers=headers, verify=False)
try:
    response = requests.get("https://classcontainers.com/api/v2.0/users", headers=headers)

    print("uname_pass: {}".format(uname_pass))
    print("headers: {}".format(headers))
    # print("response: {}".format(response))

    # print("dir(response): {}".format(dir(response)))
    json_response = response.json()
    print(json.dumps(json_response, indent=2))
except Exception as except_err:
    print("Your shit broke: {}".format(except_err))
