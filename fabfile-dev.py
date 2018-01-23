from fabric.api import *

code_path = "/home/wqh/wangqihui/work/SDATA"
env_path = "/home/wqh/wangqihui/work/env/python3_env/sdata"


def start_scrapyd():
    local(env_path + "/bin/scrapyd")


def start_rqworker():
    local(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "rqworker default high low add_spider spider_pipeline scheduler spider_status rq_worker_number_control proxy_valid")


def start_rq_scheduler():
    local(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "rqscheduler")


def start_pgadmin4():
    local(env_path + "/bin/python3.6 " + "/home/wqh/wangqihui/work/env/python3_env/pgadmin4/lib/python3.6/site-packages/pgadmin4/pgAdmin4.py")


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


def add_rq_job():
    local(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "rq_job")


def start_supervisor():
    local("supervisorctl start sdata_rq_default")


def clean_postgres():
    pass


def prepare_os():
    pass


def deploy():
    execute(pip_upgrade)

    # execute(start_scrapyd)

    # execute(start_rqworker)
    # execute(start_rq_scheduler)

    execute(add_rq_job)