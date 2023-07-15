#from Helpers.tests import *
import Helpers.tests as helperTestModule
import unittest
from io import StringIO
import sys

if __name__ == "__main__":
    reportStream = StringIO()
    runner = unittest.TextTestRunner(buffer=False,stream=reportStream,descriptions=True,verbosity=2)
    suite = unittest.TestLoader().loadTestsFromModule(helperTestModule)
    resultTest =runner.run(suite)
    
    with open("report.txt","w",encoding="utf-8") as file:
        file.write(reportStream.getvalue())


    if not resultTest.wasSuccessful():
        sys.exit(1)