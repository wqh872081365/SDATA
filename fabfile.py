from fabric.api import *

code_path = "/home/wangqihui.me/wangqihui/SDATA"
env_root = "/home/wangqihui.me/wangqihui/python/python3_env"
env_path = "/home/wangqihui.me/wangqihui/python/python3_env/SDATA"
git_repository = "git@github.com:wqh872081365/SDATA.git"

env.roledefs["apps"] = []
env.roledefs["db"] = []
env.roledefs["static"] = []
env.roledefs["job"] = []


# system
@parallel
@roles('apps')
def reload_nginx():
    sudo("nginx -s reload")


# sdata
@parallel
@roles('apps')
def pip_upgrade():
    run(env_path + "/bin/pip3.6 install -r " + code_path + "/requirements.txt")

@roles('db')
def migrate_sdata():
    run(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "migrate")

@parallel
@roles('apps')
def update_code(branch="master"):
    with cd(code_path):
        run("git pull origin %s" % (branch,))

@roles('static')
def update_static():
    run(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "collectstatic --noinput")

@parallel
@roles('apps')
def start_sdata():
    sudo("supervisorctl start sdata_gunicorn")
    sudo("rm -f " + code_path + "/maintenance.html")

@parallel
@roles('apps')
def stop_sdata():
    sudo("supervisorctl stop sdata_gunicorn")
    sudo("cp -f " + code_path + "/deploy/nginx/maintenance.html " + code_path + "/maintenance.html")

@roles('job')
def update_user_logs(user_log_id):
    run(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "update_user_logs " + user_log_id)


# rq
@parallel
@roles('apps')
def start_rq_scheduler():
    sudo("supervisorctl start sdata_rqscheduler")

@parallel
@roles('apps')
def start_rqworker():
    sudo("supervisorctl start sdata_rq_default sdata_rq_high sdata_rq_low sdata_rq_add_spider sdata_rq_spider_pipeline sdata_rq_scheduler sdata_rq_spider_status sdata_rq_worker_number_control sdata_rq_proxy_valid")

@parallel
@roles('apps')
def restart_rqworker():
    sudo("supervisorctl restart sdata_rq_default sdata_rq_high sdata_rq_low sdata_rq_add_spider sdata_rq_spider_pipeline sdata_rq_scheduler sdata_rq_spider_status sdata_rq_worker_number_control sdata_rq_proxy_valid")

@roles('job')
def add_rq_job():
    run(env_path + "/bin/python3.6 " + code_path + "/manage.py " + "rq_job")


# scrapy
@parallel
@roles('apps')
def start_scrapyd():
    sudo("supervisorctl start sdata_scrapyd")

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
    run(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py" + " del_project")

@roles('job')
def add_scrapyd_schedule(spider):
    run(env_path + "/bin/python3.6 " + code_path + "/app/utils/scrapy.py" + " add_schedule " + spider)


# postgres
@roles('db')
def start_pgadmin4():
    run(env_root + "/pgadmin4/bin/python3.6 " + env_root + "/pgadmin4/lib/python3.6/site-packages/pgadmin4/pgAdmin4.py")

@roles('db')
def clean_postgres():
    pass


# log
@parallel
@roles('apps')
def clean_log():
    pass


# update file
@parallel
@roles('apps')
def update_supervisor():
    sudo("cp -f " + code_path + "/deploy/sdata_supervisor.conf " + "/etc/supervisor/conf.d/sdata_supervisor.conf")
    sudo("supervisorctl reload")

@parallel
@roles('apps')
def update_settings():
    sudo("scp -f " + code_path + "/deploy/local_settings_aliyun.py " + "%s@%s:" % ((env.user, env.host)) + code_path + "/SDATA/local_settings.py")
    sudo("supervisorctl restart sdata_gunicorn")

@parallel
@roles('apps')
def update_nginx():
    sudo("cp -f " + code_path + "/deploy/sdata_nginx.conf " + "/etc/nginx/sites-available/sdata_nginx.conf")
    sudo("ln -sf /etc/nginx/sites-available/sdata_nginx.conf /etc/nginx/sites-enabled/sdata_nginx.conf")
    execute(reload_nginx)


# other
@parallel
@roles('apps')
def prepare_file():
    with cd("/home"):
        run("mkdir -p wangqihui.me")
        with cd("wangqihui.me"):
            run("mkdir -p wangqihui")
            with cd("wangqihui"):
                run("git clone " + git_repository)
                run("mkdir -p SDATA_LOG")
                with cd("SDATA_LOG"):
                    run("mkdir -p gunicorn")
                    with cd("gunicorn"):
                        run("touch sdata_gunicorn_stderr.log")
                        run("touch sdata_gunicorn_stdout.log")
                        run("touch sdata_gunicorn_access.log")
                    run("mkdir -p rq")
                    with cd("rq"):
                        run("touch sdata_rq_rqscheduler_stderr.log")
                        run("touch sdata_rq_rqscheduler_stdout.log")
                        run("touch sdata_rq_default_stderr.log")
                        run("touch sdata_rq_default_stdout.log")
                        run("touch sdata_rq_high_stderr.log")
                        run("touch sdata_rq_high_stdout.log")
                        run("touch sdata_rq_low_stderr.log")
                        run("touch sdata_rq_low_stdout.log")
                        run("touch sdata_rq_add_spider_stderr.log")
                        run("touch sdata_rq_add_spider_stdout.log")
                        run("touch sdata_rq_spider_pipeline_stderr.log")
                        run("touch sdata_rq_spider_pipeline_stdout.log")
                        run("touch sdata_rq_scheduler_stderr.log")
                        run("touch sdata_rq_scheduler_stdout.log")
                        run("touch sdata_rq_spider_status_stderr.log")
                        run("touch sdata_rq_spider_status_stdout.log")
                        run("touch sdata_rq_worker_number_control_stderr.log")
                        run("touch sdata_rq_worker_number_control_stdout.log")
                        run("touch sdata_rq_proxy_valid_stderr.log")
                        run("touch sdata_rq_proxy_valid_stdout.log")
                    run("mkdir -p scrapy")
                    with cd("scrapy"):
                        run("touch sdata_scrapyd_stderr.log")
                        run("touch sdata_scrapyd_stdout.log")
                run("mkdir -p python")
                with cd("python"):
                    run("mkdir -p python3_env")
                    with cd("python3_env"):
                        run("virtualenv SDATA --python=/root/.pyenv/versions/3.6.3/bin/python3.6")


@parallel
@roles('apps')
def prepare_os():
    sudo("apt-get update")
    sudo("apt-get upgrade")


@parallel
@roles('apps')
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