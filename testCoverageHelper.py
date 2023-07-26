import csv
import xml.dom.minidom
import os
import re

class CoverageHelper:


    def __init__(self,coverageDir:str) -> None:
        self.coverageDir = coverageDir
        self.coverageReport = []

    def checkCoverage(self):
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

                #parentheses ouvertes
                nbBracketOpened = 0
                # accolades ouvertes
                nbBraceOpened = 0
                # crochets ouverts
                nbHookOpened = 0

                for row in rawDataCover:
                    nbBracketOpened+=row.count("(")
                    nbBracketOpened-=row.count(")")

                    nbBraceOpened+=row.count("{")
                    nbBraceOpened-=row.count("}")

                    nbHookOpened+=row.count("[")
                    nbHookOpened-=row.count("]")


                    if row.startswith(">>>>>>"):

                        checkRow =row.split(">>>>>> ")
                        checkDeclarative = self.isDeclarationLine(checkRow[1])
                        if checkDeclarative[0]:
                            lastRowType = checkDeclarative[1]
                            rowExecuted+=1
                        elif lastRowType == "class":
                            if checkDeclarative[1] != None:
                                lastRowType =checkDeclarative[1]
                            rowExecuted+=1
                        elif lastRowType != "class":
                            lastRowType =checkDeclarative[1]
                            firstAffectComplex = "=" in row and (( row.count("(") > row.count(")")) or ( row.count("{") > row.count("}"))  or ( row.count("[") > row.count("]")))
                            closureLine = (( row.count("(") < row.count(")")) or ( row.count("{") < row.count("}"))  or ( row.count("[") < row.count("]")))
                            if (nbBracketOpened == 0 and nbBraceOpened == 0  and nbHookOpened == 0 and not closureLine) or firstAffectComplex:
                                rowNotExecuted+=1
                                #print("not executed", row, lastRowType)
                        else:
                            rowExecuted+=1
                            
                    else:
                        match =re.search("[0-9]{1,10}:",row.strip())
                        if match and match.start() == 0:
                                rowExecuted+=1

                coverageSpec = {
                    "file":el.split(".cover")[0] + ".py",
                    "coverage":str(round((rowExecuted/(rowExecuted + rowNotExecuted))*100)) + "%",
                    "rowOk":rowExecuted,
                    "rowKo":rowNotExecuted,
                    "statements":rowExecuted + rowNotExecuted

                }
                self.coverageReport.append(coverageSpec)


    def isDeclarationLine(self,rowToTest:str):
        keywords = ["class","def","import","from","if __name__ == \"__main__\":","@"]

        for k in keywords:
            if rowToTest.strip().startswith(k):
                return True, k
            
        return False, None

    def writeCoverageReport(self):
        with open ("coverage-report.csv","w",encoding="utf-8") as coverageFile:
            writer =csv.DictWriter(coverageFile,["file", "coverage","statements","rowOk","rowKo"],extrasaction="ignore",lineterminator="\n")
            writer.writeheader()
            for spec in self.coverageReport:
                writer.writerow(spec)
                

        # DOM creation
        impl = xml.dom.minidom.getDOMImplementation() 
        dom = impl.createDocument(None, 'html', impl.createDocumentType("html","",""))
        htmlNode = dom.documentElement


        head = dom.createElement('head')
        #head.setAttribute('href', 'www.google.com')
        titleTag = dom.createElement("title")
        titleTag.appendChild(dom.createTextNode('Coverage Result'))
        head.appendChild(titleTag)
        htmlNode.appendChild(head)

        body = dom.createElement('body')
        htmlNode.appendChild(body)
        tableTag = dom.createElement("table")
        body.appendChild(tableTag)
        headTable = dom.createElement("thead")
        tableTag.appendChild(headTable)
        lineHeader =dom.createElement("tr")
        headTable.appendChild(lineHeader)

        for word in ["file", "coverage","statements","rowOk","rowKo"]:

            cellHeader = dom.createElement("th")
            cellHeader.appendChild(dom.createTextNode(word))
            lineHeader.appendChild(cellHeader)


        bodyTable = dom.createElement("tbody")
        tableTag.appendChild(bodyTable)

        for spec in self.coverageReport:
            lineData = dom.createElement("tr")
            bodyTable.appendChild(lineData)
            for word in ["file", "coverage","statements","rowOk","rowKo"]:

                cellBody = dom.createElement("td")
                cellBody.appendChild(dom.createTextNode(str(spec.get(word))))
                lineData.appendChild(cellBody)


        with open ("coverage-report.html","w",encoding="utf-8") as coverageFileHtml:
            htmlFileContent =dom.toprettyxml()
            coverageFileHtml.write(htmlFileContent.split('<?xml version="1.0" ?>\n')[1])