import tests as helperTestModule
import unittest
from io import StringIO
import sys
import trace
import os
from testHelpers.testCoverageHelper import CoverageHelper

class unitTestResultWrapper:
    resutTest: unittest.TestResult

def testingProgram(resultWrapper:unitTestResultWrapper):
    reportStream = StringIO()
    runner = unittest.TextTestRunner(buffer=False,stream=reportStream,descriptions=True,verbosity=2)
    suite = unittest.TestLoader().loadTestsFromModule(helperTestModule)
    resultWrapper.resutTest=runner.run(suite)
    
    with open("reportUnitTest.txt","w",encoding="utf-8") as file:
        file.write(reportStream.getvalue())


if __name__ == "__main__":
    
    testCaseDir = os.path.join(os.getcwd(),"appHelpers","tests")

    tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix,testCaseDir],ignoremods=["testRunner"],trace=0,count=1)

    campagnTest = unitTestResultWrapper()
    # run the new command using the given tracer
    tracer.runfunc(testingProgram,campagnTest)


    # make a report, placing output in the current directory
    r = tracer.results()
    if not os.path.exists("tmpCoverage"):
        os.mkdir("tmpCoverage")
    r.write_results(show_missing=True,coverdir="tmpCoverage")

    coverageWrapper =CoverageHelper("tmpCoverage")

    coverageWrapper.checkCoverage()
    coverageWrapper.writeCoverageReport()
    

    if not campagnTest.resutTest.wasSuccessful():
        print("fail")
        sys.exit(1)
