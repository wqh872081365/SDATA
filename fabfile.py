from fabric.api import *

code_path = ""
env_path = ""

env.roledefs['apps'] = [

]


@parallel
@roles('apps')
def start_scrapyd():
    run(env_path + "/bin/scrapyd")


@parallel
@roles('apps')
def pip_upgrade():
    run(env_path + "/bin/pip3.6 install -r requirements.txt")


@parallel
@roles('apps')
def list_scrapyd_all():
    with cd(code_path + "/wdata"):
        run(env_path + "/bin/scrapyd-deploy -l")


@parallel
@roles('apps')
def scrapyd_deploy():
    with cd(code_path + "/wdata"):
        run(env_path + "/bin/scrapyd-deploy")


@parallel
@roles('apps')
def show_scrapyd_status():
    run(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py")


@parallel
@roles('apps')
def delete_scrapyd_project():
    local(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py" + " del_project")