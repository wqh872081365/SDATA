from fabric.api import *

code_path = "/home/wqh/wangqihui/work/SDATA"
env_root = "/home/wqh/wangqihui/work/env/python3_env"
env_path = "/home/wqh/wangqihui/work/env/python3_env/sdata"
git_repository = "git@github.com:wqh872081365/SDATA.git"


# system
def reload_nginx():
    local("sudo nginx -s reload")


# sdata
def pip_upgrade():
    local(env_path + "/bin/pip3.6 install -r " + code_path + "/requirements.txt")

def migrate_sdata():
    local(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "migrate")

def update_code(branch="master"):
    local("git pull origin %s" % (branch,))

def update_static():
    local(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "collectstatic --noinput")

def start_sdata():
    local("sudo supervisorctl start sdata_gunicorn")
    local("sudo rm -f " + code_path + "/maintenance.html")

def stop_sdata():
    local("sudo supervisorctl stop sdata_gunicorn")
    local("sudo cp -f " + code_path + "/templates/maintenance.html " + code_path + "/maintenance.html")

def update_user_logs(user_log_id):
    local(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "update_user_logs " + user_log_id)


# rq
def start_rq_scheduler():
    local("sudo supervisorctl start sdata_rqscheduler")

def start_rqworker():
    local("sudo supervisorctl start sdata_rq_default sdata_rq_high sdata_rq_low sdata_rq_add_spider sdata_rq_spider_pipeline sdata_rq_scheduler sdata_rq_spider_status sdata_rq_worker_number_control sdata_rq_proxy_valid")

def restart_rqworker():
    local("sudo supervisorctl restart sdata_rq_default sdata_rq_high sdata_rq_low sdata_rq_add_spider sdata_rq_spider_pipeline sdata_rq_scheduler sdata_rq_spider_status sdata_rq_worker_number_control sdata_rq_proxy_valid")

def add_rq_job():
    local(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "rq_job")


# scrapy
def start_scrapyd():
    local("sudo supervisorctl start sdata_scrapyd")

def list_scrapyd_all():
    with lcd(code_path + "/wdata"):
        local(env_path + "/bin/scrapyd-deploy -l")

def scrapyd_deploy():
    with lcd(code_path + "/wdata"):
        local(env_path + "/bin/scrapyd-deploy")

def show_scrapyd_status():
    local(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py")

def delete_scrapyd_project():
    local(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py" + " del_project")

def add_scrapyd_schedule(spider):
    local(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py" + " add_schedule " + spider)


# postgres
def start_pgadmin4():
    local(env_root + "/pgadmin4/bin/python3.6 " + env_root + "/pgadmin4/lib/python3.6/site-packages/pgadmin4/pgAdmin4.py")

def clean_postgres():
    pass


# log
def clean_log():
    pass


# update file
def update_supervisor():
    local("sudo cp -f " + code_path + "/deploy/sdata_supervisor_dev.conf " + "/etc/supervisor/conf.d/sdata_supervisor_dev.conf")
    local("sudo supervisorctl reload")

def update_settings():
    # local("sudo cp -f " + code_path + "/deploy/local_settings_aliyun.py " + code_path + "/SDATA/local_settings.py")
    local("sudo supervisorctl restart sdata_gunicorn")

def update_nginx():
    local("sudo cp -f " + code_path + "/deploy/sdata_nginx_dev.conf " + "/etc/nginx/sites-available/sdata_nginx_dev.conf")
    local("sudo ln -sf /etc/nginx/sites-available/sdata_nginx_dev.conf /etc/nginx/sites-enabled/sdata_nginx_dev.conf")
    execute(reload_nginx)


# other
def prepare_file():
    with lcd("/home"):
        local("mkdir -p wangqihui.me")
        with lcd("wanqihui.me"):
            local("mkdir -p wanqihui")
            with lcd("wanqihui"):
                local("git clone " + git_repository)
                local("mkdir -p SDATA_LOG")
                with lcd("SDATA_LOG"):
                    local("mkdir -p gunicorn")
                    local("mkdir -p rq")
                    local("mkdir -p scrapy")
                local("mkdir -p python")
                with lcd("python"):
                    local("mkdir -p python3_env")
                    with lcd("python3_env"):
                        local("pyenv shell 3.6.3")
                        local("virtualenv SDATA")
                        local("pyenv shell --unset")


def prepare_os():
    local("sudo apt-get update")
    local("sudo apt-get upgrade")


def deploy():
    execute(stop_sdata)
    execute(update_code)
    execute(pip_upgrade)
    execute(migrate_sdata)
    execute(update_static)
    execute(start_sdata)
    execute(reload_nginx)

    execute(start_rq_scheduler)
    execute(start_rqworker)
    execute(add_rq_job)

    execute(start_scrapyd)