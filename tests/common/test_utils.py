import unittest
import datetime
from hah.common import utils

class UtilsTest(unittest.TestCase):
    def test_timestamp(self):
        self.assertEqual(1420070400, utils.timestamp(datetime.datetime(2015,1,1)))
