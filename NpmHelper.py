from datetime import datetime, timedelta
from RestClient import requestWrapper



class NpmWrapper:

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

class PackageDataInfo:

    def __init__(self, rawData: dict):
        #print(rawData)
        print(rawData.keys())
        
        self.name:str =  rawData["name"]
        self.description:str= rawData.get("description","")
        self.version:str = rawData["dist-tags"]["latest"]
        if rawData.get("author"):
            self.author:str = rawData["author"]["name"]
        else:
           self.author:str = "" 
        self.license:str = rawData["license"]
        self.keywords:str = ", ".join(rawData.get("keywords",""))

        createdDatetime =datetime.strptime(rawData["time"]["created"],"%Y-%m-%dT%H:%M:%S.%fZ")
        self.createdDate:str = createdDatetime.strftime("%d/%m/%Y")

        self.readmeLines: list = rawData["readme"].split("\r\n")

class PackageDownloadInfo:
    
    def __init__(self, rawData: dict):
        self.start:str = rawData["start"]
        self.end:str = rawData["end"]
        self.name:str = rawData["package"]
        listDownload = []
        for download in rawData["downloads"]:
            listDownload.append(download["downloads"])

        self.downloads = listDownload