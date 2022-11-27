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
            print("error", rawResponse.status)
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
            print("error", rawResponse.status)
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
            print("error", rawResponse.status)
            return None

class PackageDataInfo:

    def __init__(self, rawData: dict):
        #print(rawData.keys())
        #print(rawData["time"])
        self.name:str =  rawData["name"]
        self.description:str= rawData["description"]
        self.version:str = rawData["dist-tags"]["latest"]
        self.author:str = rawData["author"]["name"]
        self.license:str = rawData["license"]
        self.keywords:str = ", ".join(rawData["keywords"])

        self.createdDate:str = rawData["time"]["created"]

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