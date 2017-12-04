# -*- coding: utf-8 -*-

import requests
import json

# scrapy api

root_url = "http://localhost:6800/"
daemon_url = root_url + "daemonstatus.json"
schedule_url = root_url + "schedule.json"


# daemonstatus
def get_daemonstatus(daemon_url=daemon_url):
    r_daemonstatus = requests.get(daemon_url)
    return json.loads(r_daemonstatus.text)


# add schedule
def add_schedule(project, spider, schedule_url=schedule_url, **kwargs):
    kwargs["project"] = project
    kwargs["spider"]= spider
    r_add_schedule = requests.post(schedule_url, data=kwargs)
    return json.loads(r_add_schedule.text)