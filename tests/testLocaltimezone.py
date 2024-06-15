from datetime import datetime
from models.LocalTimeZone import LocalTimezone
import unittest

class LocalTimeZoneTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.myTimezone = LocalTimezone()

    def test_convertUTCToTimeZoneNotDstTime(self) -> None:
        createdDatetime =datetime.strptime("2019-12-25T17:44:31.202Z","%Y-%m-%dT%H:%M:%S.%fZ")
        createdDatetime =createdDatetime.replace(tzinfo=self.myTimezone)
        createdDatetime = self.myTimezone.fromutc(createdDatetime)
        self.assertEqual(createdDatetime.hour,18)

    def test_convertUTCToTimeZoneWithDstTime(self) -> None:
        createdDatetime =datetime.strptime("2019-06-25T17:44:31.202Z","%Y-%m-%dT%H:%M:%S.%fZ")
        createdDatetime =createdDatetime.replace(tzinfo=self.myTimezone)
        createdDatetime = self.myTimezone.fromutc(createdDatetime)
        self.assertEqual(createdDatetime.hour,19)