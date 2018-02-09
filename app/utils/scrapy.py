# -*- coding: utf-8 -*-

import requests
import json
import sys
import uuid

# scrapyd api

ROOT_URL = "http://127.0.0.1:6800/"
DAEMON_URL = ROOT_URL + "daemonstatus.json"
# ADDVERSION_URL = ROOT_URL + "addversion.json"
SCHEDULE_URL = ROOT_URL + "schedule.json"
CANCEL_URL = ROOT_URL + "cancel.json"
LISTPROJECTS_URL = ROOT_URL + "listprojects.json"
LISTVERSIONS_URL = ROOT_URL + "listversions.json"
LISTSPIDERS_URL = ROOT_URL + "listspiders.json"
LISTJOBS_URL = ROOT_URL + "listjobs.json"
DELVERSION_URL = ROOT_URL + "delversion.json"
DELPROJECT_URL = ROOT_URL + "delproject.json"

PROXY_LIST = [
    # "data5u",
    # "xici",
    "proxydb"
]

PROXY_NAME_LIST = ["data5u", "xici", "proxydb"]

JOB_DICT = {
    "data5u": "",
    "xici": "",
    "proxydb": "",
    "BilibiliSeason": "",
    "BilibiliSeasonHigh": "",
}

PROJECT_DICT = {
    "wdata": "wdata"
}


def get_daemonstatus(daemon_url=DAEMON_URL):
    r_daemonstatus = requests.get(daemon_url)
    return json.loads(r_daemonstatus.text)


# def add_version(project, version, egg, addversion_url=ADDVERSION_URL, **kwargs):
#     kwargs["project"] = project
#     kwargs["version"]= version
#     files = {"egg": open(egg, "rb")}
#     r_add_version = requests.post(addversion_url, data=kwargs, files=files)
#     return json.loads(r_add_version.text)


def add_schedule(project, spider, jobid="", schedule_url=SCHEDULE_URL, **kwargs):
    if not jobid:
        jobid = uuid.uuid1().hex
    kwargs["project"] = project
    kwargs["spider"] = spider
    kwargs["jobid"] = jobid
    r_add_schedule = requests.post(schedule_url, data=kwargs)
    return json.loads(r_add_schedule.text)


def remove_schedule(project, job, cancel_url=CANCEL_URL, **kwargs):
    kwargs["project"] = project
    kwargs["job"] = job
    r_remove_schedule = requests.post(cancel_url, data=kwargs)
    return json.loads(r_remove_schedule.text)


def list_projects(listprojects_url=LISTPROJECTS_URL):
    r_listprojects = requests.get(listprojects_url)
    return json.loads(r_listprojects.text)


def list_versions(project, listversions_url=LISTVERSIONS_URL):
    r_listversions = requests.get(listversions_url, params={"project": project})
    return json.loads(r_listversions.text)


def list_spiders(project, listspiders_url=LISTSPIDERS_URL):
    r_listspiders = requests.get(listspiders_url, params={"project": project})
    return json.loads(r_listspiders.text)


def list_jobs(project, listjobs_url=LISTJOBS_URL):
    r_listjobs = requests.get(listjobs_url, params={"project": project})
    return json.loads(r_listjobs.text)


def del_version(project, version, delversion_url=DELVERSION_URL):
    r_delversion = requests.post(delversion_url, data={"project": project, "version": version})
    return json.loads(r_delversion.text)


def del_project(project, delproject_url=DELPROJECT_URL):
    r_delproject = requests.post(delproject_url, data={"project": project})
    return json.loads(r_delproject.text)


def del_old_version():
    pass


def del_old_versions():
    pass


def spider_is_run():
    pass


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "del_project":
            print(del_project("wdata"))
        elif sys.argv[1] == "add_schedule" and len(sys.argv) == 3 and sys.argv[2] in JOB_DICT:
            job_id = uuid.uuid1().hex
            print(add_schedule("wdata", sys.argv[2], job_id, **{"job_id": job_id}))
        else:
            print("fab error")
    else:
        print("daemonstatus: ", get_daemonstatus())
        projects = list_projects()
        print("projects: ", projects)
        print("project wdata versions: ", list_versions("wdata"))
        if projects.get("status", "") == "ok" and "wdata" in projects.get("projects", []):
            print("project wdata spiders: ", list_spiders("wdata"))
            print("project wdata jobs: ", list_jobs("wdata"))


if __name__ == "__main__":
    # main()
    job_id = uuid.uuid1().hex
    # print(add_schedule("wdata", "proxydb", job_id))
    # print(add_schedule("wdata", "BilibiliSeason", job_id, **{"job_id": job_id}))
    # print(add_schedule("wdata", "BilibiliSeason", job_id, **{"page": "1", "job_id": job_id}))
    # print(add_schedule("wdata", "BilibiliSeason", job_id,
    #                    **{"type": "2", "season_id_list": "21603", "job_id": job_id}))
    # print(add_schedule("wdata", "BilibiliSeason", job_id,
    #                    **{"type": "1", "old_user_log_id": "46", "job_id": job_id}))
    # print(add_schedule("wdata", "BilibiliSeasonHigh", job_id,
    #                    **{"type": "2", "season_id_list": "21603", "job_id": job_id}))
    pass
