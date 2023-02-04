from datetime import datetime, timedelta
from Helpers.HttpClient import requestWrapper
from models.NpmModels import PackageDataInfo, PackageDownloadInfo


class NpmHelper:

    _baseUrlInfo: str = "https://registry.npmjs.org/"
    _baseUrlDownloadCount: str = "https://api.npmjs.org/downloads/range/"

    def getPackageGeneralInfo(self,packageName: str):
        rawResponse = requestWrapper(self._baseUrlInfo + packageName)
        if rawResponse.status == 200:

            possibleData = rawResponse.json()
            if len(possibleData) > 0:
                return PackageDataInfo(possibleData)
        else:
            print("error infos", rawResponse.status, rawResponse.body)
            return None

    def getLast30daysDownload(self, packageName:str):
        now = datetime.now()
        ThirtyDaysAgo =now - timedelta(days=30)
        rawResponse = requestWrapper(self._baseUrlDownloadCount + ThirtyDaysAgo.strftime("%Y-%m-%d") + ":" + now.strftime("%Y-%m-%d") + "/" + packageName)
        if rawResponse.status == 200:

            possibleData = rawResponse.json()
            if len(possibleData) > 0:
                return PackageDownloadInfo(possibleData)
        else:
            print("error 30", rawResponse.status, rawResponse.body)
            return None

    def getLast7daysDownload(self, packageName:str):
        now = datetime.now()
        SevenDaysAgo =now - timedelta(days=7)
        rawResponse = requestWrapper(self._baseUrlDownloadCount + SevenDaysAgo.strftime("%Y-%m-%d") + ":" + now.strftime("%Y-%m-%d") + "/" + packageName)
        if rawResponse.status == 200:

            possibleData = rawResponse.json()
            if len(possibleData) > 0:
                return PackageDownloadInfo(possibleData)
        else:
            print("error 7 days", rawResponse.status, rawResponse.body)
            return None

    def getDownloadBetween2Date(self, packageName:str,startPeriod:datetime, endPeriod:datetime):
        rawResponse = requestWrapper(self._baseUrlDownloadCount + startPeriod.strftime("%Y-%m-%d") + ":" + endPeriod.strftime("%Y-%m-%d") + "/" + packageName)
        if rawResponse.status == 200:

            possibleData = rawResponse.json()
            if len(possibleData) > 0:
                return PackageDownloadInfo(possibleData)
        else:
            print("error between", rawResponse.status, rawResponse.body)
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

