from django.test import TestCase
from app.logs.add_log import add_spider_log
from scrapy.http import Response
# Create your tests here.


class UserLogTestCase(TestCase):

    def setUp(self):
        pass

    def test_add_spider_log(self):
        log = add_spider_log(user_log_id=1, source="0", source_id=1, url="test_url", status="2", msg="test_msg", response=Response(url="test_url", body="test_body".encode("utf-8")))
        self.assertEqual(log.logs.get("fg_msg")[0].get("msg", "") if log.logs and isinstance(log.logs, (dict,)) and log.logs.get("fg_msg", []) and isinstance(log.logs.get("fg_msg", []), (list, tuple)) and log.logs.get("fg_msg")[0] and isinstance(log.logs.get("fg_msg")[0], dict) else "", "test_msg")
        self.assertEqual(log.logs.get("fg_msg")[0].get("url", "") if log.logs and isinstance(log.logs, (dict,)) and log.logs.get("fg_msg", []) and isinstance(log.logs.get("fg_msg", []), (list, tuple)) and log.logs.get("fg_msg")[0] and isinstance(log.logs.get("fg_msg")[0], dict) else "", "test_url")
        self.assertEqual(log.logs.get("fg_msg")[0].get("data", "") if log.logs and isinstance(log.logs, (dict,)) and log.logs.get("fg_msg", []) and isinstance(log.logs.get("fg_msg", []), (list, tuple)) and log.logs.get("fg_msg")[0] and isinstance(log.logs.get("fg_msg")[0], dict) else "", "test_body")