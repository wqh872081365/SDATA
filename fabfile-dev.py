from fabric.api import *

code_path = "/home/wqh/wangqihui/work/SDATA"
env_path = "/home/wqh/wangqihui/work/env/python3_env/sdata"


def start_scrapyd():
    local(env_path + "/bin/scrapyd")


def pip_upgrade():
    local(env_path + "/bin/pip3.6 install -r requirements.txt")


def list_scrapyd_all():
    local(env_path + "/bin/scrapyd-deploy -l")


def scrapyd_deploy():
    local(env_path + "/bin/scrapyd-deploy")


def show_scrapyd_status():
    local(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py")


def delete_scrapyd_project():
    local(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py" + " del_project")


def add_scrapyd_schedule(spider):
    local(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py" + " add_schedule " + spider)