from Helpers.NpmHelper import NpmHelper
from threading import Thread
from datetime import datetime
from models.CustomExceptions import UnpublishedPackage


class GetNpmDataThread(Thread):
    """
    Thread to get npm data
    """
    def __init__(self,npmPackage:str ):
        super().__init__()
        #self.gui = app2Update
        self.packageName =npmPackage
        self.dataToShow = None
        self.listDownloadsThirty = None
        self.hasError = False
        self.errMsg = ""
        self.nbTotalDownload = 0



    def run(self):
        npmInfoClient = NpmHelper()
        try:
            self.dataToShow = npmInfoClient.getPackageGeneralInfo(self.packageName)
            if not self.dataToShow:
                #self.gui.after(0,self.gui.showPopupError())
                self.hasError = True
                self.errMsg = "Une erreur est survenue dans la récupération des données"
            else:
                #self.gui.after(0, self.gui.updateGeneralInfoTab(dataToShow))
                now = datetime.now()
                createdAt = datetime.strptime(self.dataToShow.createdDate,"%d/%m/%Y")

                
                listInterval =NpmHelper.getListIntervalOneYearNpm(createdAt,now)
                for interval in listInterval:
                    downloadTmp = npmInfoClient.getDownloadBetween2Date(self.dataToShow.name,interval.get("start"), interval.get("end"))
                    if downloadTmp:
                        self.nbTotalDownload += sum(downloadTmp.listDownload)

                # get last 30 days
                self.listDownloadsThirty = npmInfoClient.getLast30daysDownload(self.dataToShow.name)
                

        except UnpublishedPackage as ex:
            self.hasError = True
            self.errMsg = ex.message

        except Exception as e:
            self.hasError = True
            self.errMsg = str(e)
