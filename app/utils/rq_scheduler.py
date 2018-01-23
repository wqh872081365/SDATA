# -*- coding: utf-8 -*-
import django_rq
from app.utils.scrapy import list_projects, list_jobs
from app.logs.models import UserLog
from app.logs.add_log import update_user_log

SCHEDULER_LIST = ["scheduler", "spider_status"]


def add_spider_status_scheduler():
    projects_result = list_projects()
    print("projects_result: ", projects_result)
    project_list = projects_result.get("projects", [])
    if projects_result.get("status", "") == "ok":
        for project in project_list:
            jobs_result = list_jobs(project)
            print("project %s jobs: " % (project,), jobs_result)
            pending_job_list = jobs_result.get("pending", [])
            running_job_list = jobs_result.get("running", [])
            finished_job_list = jobs_result.get("finished", [])
            finished_job_list.sort(key=lambda x: x["end_time"], reverse=True)
            print("finished_job_list: ", finished_job_list[:100])
            finished_id_dict = {job.get("id", ""): "finished" for job in finished_job_list if job.get("id", "")}
            if jobs_result.get("status", "") == "ok":
                not_finish_log_list = UserLog.objects.filter(status__in=["1", "5"])
                for user_log in not_finish_log_list:
                    job_id = user_log.logs.get("job_id", "")
                    if finished_id_dict.get(job_id, "") == "finished":
                        update_user_log(user_log.id)
                        print("user_log_id %s job_id %s status %s finished ok" % (user_log.id, job_id, user_log.status))
            else:
                print("list jobs is failed")
    else:
        print("list projects is failed")


def list_rq_scheduler(until=None):
    if until:
        kwargs = {"until": until}
    else:
        kwargs = {}
    for scheduler_name in SCHEDULER_LIST:
        scheduler = django_rq.get_scheduler(scheduler_name)
        list_of_job_instances = scheduler.get_jobs(with_times=True, **kwargs)
        print("scheduler_name: ", list_of_job_instances)


def scheduler_cancel(scheduler_name, job_id):
    scheduler = django_rq.get_scheduler(scheduler_name)
    if job_id in scheduler:
        scheduler.cancel(job_id)
        print(scheduler_name, job_id, "cannel ok")
    else:
        print("%s not find in %s" % (job_id, scheduler_name))