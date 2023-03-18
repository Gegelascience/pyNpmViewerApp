from Helpers.NpmHelper import NpmHelper
from threading import Thread
from datetime import datetime
from Helpers.CustomExceptionHelper import UnpublishedPackage

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.mainView import MyApp




class GetNpmDataThread(Thread):
    """
    Thread to get npm data
    """
    def __init__(self, app2Update:"MyApp",npmPackage:str ):
        super().__init__()
        self.gui = app2Update
        self.packageName =npmPackage


    def run(self):
        npmInfoClient = NpmHelper()
        try:
            dataToShow = npmInfoClient.getPackageGeneralInfo(self.packageName)
            if not dataToShow:
                self.gui.after(0,self.gui.showPopupError())
            else:
                self.gui.after(0, self.gui.updateGeneralInfoTab(dataToShow))
                now = datetime.now()
                createdAt = datetime.strptime(dataToShow.createdDate,"%d/%m/%Y")

                nbTotalDownload = 0
                listInterval =NpmHelper.getListIntervalOneYearNpm(createdAt,now)
                for interval in listInterval:
                    downloadTmp = npmInfoClient.getDownloadBetween2Date(dataToShow.name,interval.get("start"), interval.get("end"))
                    if downloadTmp:
                        nbTotalDownload += sum(downloadTmp.downloads)

                # get last 7 days graph
                listDownloadsSeven = npmInfoClient.getLast7daysDownload(dataToShow.name)

                listDownloadsThirty = npmInfoClient.getLast30daysDownload(dataToShow.name)

                self.gui.after(0, self.gui.updateDownloadInfoTab(dataToShow,nbTotalDownload,listDownloadsSeven,listDownloadsThirty))

        except UnpublishedPackage as ex:
            self.gui.after(0,self.gui.showPopupError(ex.message))