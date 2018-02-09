# -*- coding: utf-8 -*-
from django.utils import timezone
from django.conf import settings
from app.logs.models import SpiderLog, UserLog
from app.video.models import BilibiliSeason
from app.utils.scrapy import list_projects, list_jobs, get_daemonstatus


def add_spider_log(user_log_id, source, source_id, url, status, msg, response, type="fg_msg"):
    if not isinstance(type, (str,)):
        type = "fg_msg"
    logs = {
        "time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT),
        type: [{
            "msg": msg,
            "url": response.url,
            "data": response.body.decode("utf-8"),
            "time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)
        }]}
    log = SpiderLog(user_log_id=user_log_id, source=source, source_id=source_id, url=url, status=status, logs=logs)
    log.save()
    return log


def add_user_log(project, spider, job_id, type, count, discription, status="5", user_id=settings.USER_ID):
    logs = {
        "project": project,
        "spider": spider,
        "job_id": job_id,
        "start_time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT),
        "discription": discription,
        "undone": discription,
        # "failed": [],
        # "success": [],
    }
    log = UserLog(user_id=user_id, log_type=type, status=status, logs=logs, count=count, success=0)
    log.save()
    return log


def add_msg(user_log, msg, response, type="fg_msg", source="spider"):
    if source == "pipeline":
        log = {
            "msg": msg,
            "url": "",
            "data": response if response else "",
            "time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)
        }
        if not isinstance(type, (str,)):
            type = "fg_msg"
        if user_log.success_detail.get(type) and isinstance(user_log.success_detail[type], (tuple, list)):
            user_log.success_detail[type].append(log)
        else:
            user_log.success_detail[type] = [log, ]
    else:
        log = {
            "msg": msg,
            "url": response.url if response else "",
            "data": response.body.decode("utf-8") if response else "",
            "time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)
        }
        if not isinstance(type, (str,)):
            type = "fg_msg"
        if user_log.logs.get(type) and isinstance(user_log.logs[type], (tuple, list)):
            user_log.logs[type].append(log)
        else:
            user_log.logs[type] = [log]
    return user_log


def add_end(user_log):
    user_log.success_detail["end_time"] = timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)
    return user_log


def clean_log():
    pass


def show_spider_log(user_log_id):
    pass


def update_user_log(user_log_id):
    try:
        user_log = UserLog.objects.get(id=user_log_id)
        if user_log.status == "1":
            user_log.status = "2"
        discription = user_log.logs["discription"]
        success_detail = []
        for season_id in discription:
            if find_user_log_in_season(user_log_id, season_id):
                success_detail.append(season_id)
        user_log.success = len(success_detail)
        user_log.success_detail = {
            "success": success_detail,
            "update_time": timezone.localtime(timezone.now()).strftime(settings.LOG_DATE_FORMAT)
        }
        if len(success_detail) == len(discription):
            user_log.success_detail["complete"] = True
        user_log.save(update_fields=['success', 'status', 'success_detail'])
    except Exception as e:
        print(e)


def find_user_log_in_season(user_log_id, season_id):
    try:
        season = BilibiliSeason.objects.get(season_id=season_id)
        for data in reversed(season.detail["details"]):
            if data.get("user_log_id") == user_log_id:
                return True
        return False
    except Exception as e:
        print(e)


def update_user_logs(user_log_id=""):
    try:
        if user_log_id:
            user_log_one = UserLog.objects.get(id=int(user_log_id))
            project_one = user_log_one.logs.get("project", "")
            if project_one:
                project_list = [project_one]
            else:
                user_log_one = None
                projects_result = list_projects()
                print("projects_result: ", projects_result)
                project_list = projects_result.get("projects", []) if projects_result.get("status", "") == "ok" else []
        else:
            user_log_one = None
            projects_result = list_projects()
            print("projects_result: ", projects_result)
            project_list = projects_result.get("projects", []) if projects_result.get("status", "") == "ok" else []
        if project_list:
            for project in project_list:
                jobs_result = list_jobs(project)
                print("project %s jobs: " % (project,), jobs_result)
                # pending_job_list = jobs_result.get("pending", [])
                # running_job_list = jobs_result.get("running", [])
                finished_job_list = jobs_result.get("finished", [])
                finished_job_list.sort(key=lambda x: x["end_time"], reverse=True)
                print("finished_job_list: ", finished_job_list[:100])
                finished_id_dict = {job.get("id", ""): "finished" for job in finished_job_list if job.get("id", "")}
                if jobs_result.get("status", "") == "ok":
                    if user_log_one:
                        not_finish_log_list = [user_log_one, ]
                    else:
                        not_finish_log_list = UserLog.objects.filter(status__in=["1", "5"], logs__project="project")
                    for user_log in not_finish_log_list:
                        job_id = user_log.logs.get("job_id", "")
                        if finished_id_dict.get(job_id, "") == "finished":
                            update_user_log(user_log.id)
                            print("user_log_id %s job_id %s status %s finished ok" % (user_log.id, job_id,
                                                                                      user_log.status))
                else:
                    print("list jobs is failed")
        else:
            print("list projects is failed")
    except Exception as e:
        print(e)


def count_not_finish_user_logs():
    user_log_count = UserLog.objects.filter(status__in=["1", "5"]).count()
    print("user log not finish count %s" % (user_log_count,))
    if user_log_count:
        return
    status_result = get_daemonstatus()
    print("get_daemonstatus: ", status_result)
    if status_result.get("status", "") == "ok":
        finishing_job_count = status_result.get("finished", 0)
        pending_job_count = status_result.get("pending", 0)
        running_job_count = status_result.get("running", 0)
        if pending_job_count or pending_job_count:
            print("pending_job_count %s, running_job_count %s." % (pending_job_count, running_job_count))
            return
        if finishing_job_count > 100:
            print("user log all finish and scrapyd hava no job, finish job count %s, "
                  "you can clean job by restart scrapyd service." % (finishing_job_count,))
            return
        else:
            print("user log all finish and scrapyd hava no job.")
            return
    else:
        print("get daemonstatus failed")
        return
