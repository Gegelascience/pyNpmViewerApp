from datetime import datetime
from models.CustomExceptions import UnpublishedPackage
from models.LocalTimeZone import LocalTimezone
from dataclasses import dataclass

class PackageDataInfo:

    def __init__(self, rawData: dict, isPackageIntegrityOk=False):
        
        self.name:str =  rawData["name"]
        self.description:str= rawData.get("description","")
        if not rawData.get("dist-tags"):
            raise UnpublishedPackage(self.name)
        self.version:str = rawData["dist-tags"]["latest"]
        if rawData.get("author"):
            self.contributors:str = rawData["author"]["name"]
        elif rawData.get("maintainers",[]):
            self.contributors:str = ", ".join([maintainer.get("name") for maintainer in rawData.get("maintainers",[])])
        else:
           self.contributors:str = "" 
        self.license:str = rawData.get("license","")
        self.keywords:str = ", ".join(rawData.get("keywords",""))

        createdDatetime =datetime.strptime(rawData["time"]["created"],"%Y-%m-%dT%H:%M:%S.%fZ")
        myTimezone = LocalTimezone()

        createdDatetime = createdDatetime.replace(tzinfo=myTimezone)
        createdDatetime = myTimezone.fromutc(createdDatetime)
        
        self.createdDate:str = createdDatetime.strftime("%d/%m/%Y")

        readMeStr:str = rawData.get("readme","")
        if len(readMeStr) == 0:
            versionsKeys:list =sorted(rawData.get("versions").keys(),reverse=True)
            for version in versionsKeys:
                if len(rawData.get("versions")[version].get("readme",""))> 0:
                    readMeStr =rawData.get("versions")[version].get("readme","")
                    break

        if len(readMeStr.split("\r\n")) > 1:
            self.readmeLines: list = readMeStr.split("\r\n")
        else:
            self.readmeLines: list = readMeStr.split("\n")

        self.lastVersionIntegrity = isPackageIntegrityOk

@dataclass
class PackageDownloadInfo:
    start:str
    end:str
    name:str
    listDownload: list
    listDays: list
    