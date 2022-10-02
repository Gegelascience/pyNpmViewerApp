from RestClient import requestWrapper



class NpmWrapper:

    _baseUrlInfo: str = "https://registry.npmjs.org/"
    _baseUrlDownloadCount: str = "https://api.npmjs.org/downloads/range/"

    def getPackageGeneralInfo(self,packageName: str):
        rawResponse = requestWrapper(self._baseUrlInfo + packageName)
        if rawResponse.status == 200:

            possibleData = rawResponse.json()
            if len(possibleData) > 0:
                print(possibleData)
        else:
            print("error", rawResponse.status)




test = NpmWrapper()

test.getPackageGeneralInfo("ngx-view360")
