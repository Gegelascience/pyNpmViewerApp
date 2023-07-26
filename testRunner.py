#from Helpers.tests import *
import Helpers.tests as helperTestModule
import unittest
from io import StringIO
import sys
import trace
import os
from testCoverageHelper import CoverageHelper

def testingProgram(dicResultTest:dict):
    reportStream = StringIO()
    runner = unittest.TextTestRunner(buffer=False,stream=reportStream,descriptions=True,verbosity=2)
    suite = unittest.TestLoader().loadTestsFromModule(helperTestModule)
    dicResultTest["result"] =runner.run(suite)
    
    with open("reportUnitTest.txt","w",encoding="utf-8") as file:
        file.write(reportStream.getvalue())


if __name__ == "__main__":
    
    testCaseDir = os.path.join(os.getcwd(),"Helpers","tests")

    tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix,testCaseDir],ignoremods=["testRunner"],trace=0,count=1)

    dicResultTest = {"result":None}
    # run the new command using the given tracer
    tracer.runfunc(testingProgram,dicResultTest)


    # make a report, placing output in the current directory
    r = tracer.results()
    if not os.path.exists("tmpCoverage"):
        os.mkdir("tmpCoverage")
    r.write_results(show_missing=True,coverdir="tmpCoverage")

    coverageWrapper =CoverageHelper("tmpCoverage")

    coverageWrapper.checkCoverage()
    coverageWrapper.writeCoverageReport()

    

    if not dicResultTest["result"].wasSuccessful():
        sys.exit(1)
