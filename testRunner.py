#from Helpers.tests import *
import Helpers.tests as helperTestModule
import unittest
from io import StringIO
import sys
import trace
import os
import re
import csv

def testingProgram(dicResultTest:dict):
    reportStream = StringIO()
    runner = unittest.TextTestRunner(buffer=False,stream=reportStream,descriptions=True,verbosity=2)
    suite = unittest.TestLoader().loadTestsFromModule(helperTestModule)
    dicResultTest["result"] =runner.run(suite)
    
    with open("reportUnitTest.txt","w",encoding="utf-8") as file:
        file.write(reportStream.getvalue())

def isDeclarationLine(rowToTest:str):
    keywords = ["class","def","import","from","if __name__ == \"__main__\":","@"]

    for k in keywords:
        if rowToTest.strip().startswith(k):
            return True, k
        
    return False, None

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
    r.write_results(show_missing=True, summary=True,coverdir="tmpCoverage")

    coverageReport = []
    coverageDir = os.path.join(os.getcwd(),"tmpCoverage")
    for el in os.listdir(coverageDir):
        if el.endswith(".cover"):
            with open(os.path.join(coverageDir, el),encoding="utf-8") as coverfile:
                rawDataCover = coverfile.readlines()
            fileRowLen = len(rawDataCover)
            
            ignoredRow =0
            rowExecuted =0
            rowNotExecuted =0
            lastRowType = None
            for row in rawDataCover:
                if row.startswith(">>>>>>"):

                    checkRow =row.split(">>>>>> ")
                    checkDeclarative = isDeclarationLine(checkRow[1])
                    if checkDeclarative[0]:
                        lastRowType = checkDeclarative[1]
                        rowExecuted+=1
                    elif lastRowType == "class":
                        if checkDeclarative[1] != None:
                            lastRowType =checkDeclarative[1]
                        rowExecuted+=1
                    else:
                        if lastRowType != "class":
                            lastRowType =checkDeclarative[1]
                            rowNotExecuted+=1
                            print("not executed", row, lastRowType)
                        else:
                            rowExecuted+=1
                        
                else:
                    match =re.search("[0-9]{1,10}:",row.strip())
                    if match and match.start() == 0:
                            rowExecuted+=1

            coverageSpec = {
                "file":el,
                "coverage":(rowExecuted/(rowExecuted + rowNotExecuted))*100,
                "rowOk":rowExecuted,
                "rowKo":rowNotExecuted,
                "statements":rowExecuted + rowNotExecuted

            }
            coverageReport.append(coverageSpec)

    with open ("coverage-report.csv","w",encoding="utf-8") as coverageFile:
        writer =csv.DictWriter(coverageFile,["file", "coverage","statements","rowOk","rowKo"],extrasaction="ignore",lineterminator="\n")
        writer.writeheader()
        for spec in coverageReport:
            writer.writerow(spec)
            




    if not dicResultTest["result"].wasSuccessful():
        sys.exit(1)
