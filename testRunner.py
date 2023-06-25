from Helpers.tests import *
import unittest
from io import StringIO

if __name__ == "__main__":
    reportTest = StringIO()
    runner = unittest.TextTestRunner(reportTest,descriptions=True,verbosity=2)
    unittest.main(verbosity=2,buffer=False,exit=False, testRunner=runner)

    with open("report.txt","w",encoding="utf-8") as file:
        file.write(reportTest.getvalue())