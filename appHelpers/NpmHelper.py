from datetime import datetime, timedelta
from appHelpers.HttpClient import requestWrapper
from models.NpmModels import PackageDataInfo, PackageDownloadInfo
import hashlib
import base64

class NpmHelper:

    _baseUrlInfo: str = "https://registry.npmjs.org/"
    _baseUrlDownloadCount: str = "https://api.npmjs.org/downloads/range/"

    def getPackageGeneralInfo(self,packageName: str):
        rawResponse = requestWrapper(self._baseUrlInfo + packageName)
        if rawResponse.status == 200:
            try:
                possibleData = rawResponse.json()
                if len(possibleData) > 0:
                    integrityOk= self.checkPackageIntegrity(possibleData)
                    return PackageDataInfo(possibleData,integrityOk)
            except Exception as e:
                print(e)
                return None
        else:
            print("error infos", rawResponse.status, rawResponse.body)
            return None

    def getLast30daysDownload(self, packageName:str):
        now = datetime.now()
        ThirtyDaysAgo =now - timedelta(days=30)
        rawResponse = requestWrapper(self._baseUrlDownloadCount + ThirtyDaysAgo.strftime("%Y-%m-%d") + ":" + now.strftime("%Y-%m-%d") + "/" + packageName)
        if rawResponse.status == 200:
            try:
                possibleData = rawResponse.json()
                if len(possibleData) > 0:
                    downloadsNb = [download.get("downloads") for download in possibleData.get("downloads")]
                    downloadsDays = [download.get("day") for download in possibleData.get("downloads")]
                    return PackageDownloadInfo(possibleData.get("start"),possibleData.get("end"),possibleData.get("package"),downloadsNb,downloadsDays)
            except:
                return None
        else:
            print("error 30", rawResponse.status, rawResponse.body)
            return None

    def getLast7daysDownload(self, packageName:str):
        now = datetime.now()
        SevenDaysAgo =now - timedelta(days=7)
        rawResponse = requestWrapper(self._baseUrlDownloadCount + SevenDaysAgo.strftime("%Y-%m-%d") + ":" + now.strftime("%Y-%m-%d") + "/" + packageName)
        if rawResponse.status == 200:
            try:
                possibleData = rawResponse.json()
                if len(possibleData) > 0:
                    downloadsNb = [download.get("downloads") for download in possibleData.get("downloads")]
                    downloadsDays = [download.get("day") for download in possibleData.get("downloads")]
                    return PackageDownloadInfo(possibleData.get("start"),possibleData.get("end"),possibleData.get("package"),downloadsNb,downloadsDays)
            except:
                return None
        else:
            print("error 7 days", rawResponse.status, rawResponse.body)
            return None

    def getDownloadBetween2Date(self, packageName:str,startPeriod:datetime, endPeriod:datetime):
        if endPeriod.year < 2015:
            print("pas de stats avant 2015")
            return None
        rawResponse = requestWrapper(self._baseUrlDownloadCount + startPeriod.strftime("%Y-%m-%d") + ":" + endPeriod.strftime("%Y-%m-%d") + "/" + packageName)
        if rawResponse.status == 200:
            try:
                possibleData = rawResponse.json()
                if len(possibleData) > 0:
                    downloadsNb = [download.get("downloads") for download in possibleData.get("downloads")]
                    downloadsDays = [download.get("day") for download in possibleData.get("downloads")]
                    return PackageDownloadInfo(possibleData.get("start"),possibleData.get("end"),possibleData.get("package"),downloadsNb,downloadsDays)
            except:
                return None
        else:
            print("error between", rawResponse.status, rawResponse.body, startPeriod, endPeriod)
            return None
        

    def getListIntervalOneYearNpm(start:datetime,end:datetime) -> list:
        listInterval = []

        indexDate = start
        indexYear = start.year
        while indexYear != end.year:
            lastDayOfYear = datetime.strptime("31/12/" + str(indexYear),"%d/%m/%Y")
            listInterval.append({"start":indexDate, "end":lastDayOfYear})
            indexYear+=1
            indexDate = datetime.strptime("01/01/" + str(indexYear),"%d/%m/%Y")
    
        #annee de fin
        listInterval.append({"start":indexDate, "end":end})
    
        return listInterval
    
    def checkPackageIntegrity(self,rawInfoNpm:dict):
        if rawInfoNpm:
            try:
                lastVersionTag = rawInfoNpm.get("dist-tags",{}).get("latest")
                if lastVersionTag:
                    lastVersion = rawInfoNpm.get("versions",{}).get(lastVersionTag)
                    tarballUrl = lastVersion.get("dist").get("tarball")
                    integrityTest = lastVersion.get("dist").get("integrity")

                    rawResponse = requestWrapper(tarballUrl)
                    if rawResponse.status == 200:
                        binaryToCheck = rawResponse.raw()
                        digestData = base64.b64encode(hashlib.sha512(binaryToCheck).digest())
                        if integrityTest.split("-")[0] == "sha512" and integrityTest.split("-")[1] == digestData.decode("utf-8"):
                            return True

            except Exception as ex:
                print("ex", ex)
                return False 
            
        return False


