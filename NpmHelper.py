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


class PackageDataInfo:

    def __init__(self, rawData: dict):
        print(rawData.keys())
        self.name =  rawData["name"]
        self.description= rawData["description"]
        print(rawData["dist-tags"])
        #self.version= rawData["versions"]
        self.version= rawData["dist-tags"]["latest"]
        self.author= rawData["author"]["name"]


