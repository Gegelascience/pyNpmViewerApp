from Helpers.NpmHelper import NpmHelper
import unittest
from datetime import datetime

class NpmHelperTestCase(unittest.TestCase):

    def setUp(self):
        #self.npmHelper = NpmHelper()
        self.startDate = datetime.strptime("01/01/1995", "%d/%m/%Y")
        self.endDate = datetime.strptime("01/01/1996", "%d/%m/%Y")

    def test_getListIntervalOneYearNpm(self):
        nbYear = NpmHelper.getListIntervalOneYearNpm(self.startDate,self.endDate)
        self.assertEqual(len(nbYear),2)