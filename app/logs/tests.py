from django.test import TestCase
from app.logs.models import UserLog
from fabfile_dev import start_scrapyd
# Create your tests here.


class UserLogTestCase(TestCase):

    def setUp(self):
        pass


    def test_find_user_log_in_season(self):
        pass