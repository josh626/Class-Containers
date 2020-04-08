import json
from flask import Flask
from flask import render_template
from modules import cc_get # as cc_get
cc = Flask(__name__)

@cc.route('/')
def index():
    cc_projects = cc_get.get_projects()
    return render_template('index.html', cc_projects=cc_projects, value1="This is a Rendered Value!!!")

if __name__ == '__main__':
    cc.run(host='0.0.0.0')
