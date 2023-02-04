from datetime import datetime

class PackageDataInfo:

    def __init__(self, rawData: dict):
        #print(rawData)
        
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