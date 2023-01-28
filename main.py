from tkinter import Tk, ttk
from tkinter import *
from InfoNpmWidgets import InfoPackageWidget,GraphDownloadsWidget
from NpmHelper import NpmWrapper
from threading import Thread
from datetime import datetime

class MyApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("Informations Package NPM")

        self.geometry('600x800')

        ttk.Label(self,text="Renseigner le nom du package").pack()
        
        # ajout du champ formulaire
        self.package = StringVar()
        package_entry = ttk.Entry(self, width=20, textvariable=self.package)
        package_entry.pack()
        
        ttk.Button(self, text="Rechercher", command=self.showInformation).pack()


        tabControl = ttk.Notebook(self)
  
        self.tabInfo = ttk.Frame(tabControl)
        self.tabDownload = ttk.Frame(tabControl)

        tabControl.add(self.tabInfo, text ='Informations')
        tabControl.add(self.tabDownload, text ='Téléchargements')
        tabControl.pack(expand = 1, fill ="both")

        package_entry.focus()

    def showInformation(self):
        packageName = self.package.get()
        npmThread = GetNpmDataThread(self,packageName)
        npmThread.start()

    def updateGeneralInfoTab(self, dataFromNpm):
        for child in self.tabInfo.winfo_children():
            child.destroy()
        InfoPackageWidget(self.tabInfo, dataFromNpm).pack()

    def updateDownloadInfoTab(self, generalDataFromNpm, sumDownload, lastSevenDays):

        for child in self.tabDownload.winfo_children():
            child.destroy()
        GraphDownloadsWidget(self.tabDownload, generalDataFromNpm, sumDownload,lastSevenDays).pack()	

    def showPopuError(self):
        ErrorPopup(self)

        


class ErrorPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("ERREUR")
        self.geometry('150x50')
        ttk.Label(self,text="Une erreur est survenue").pack()


class GetNpmDataThread(Thread):
    def __init__(self, app2Update:MyApp,npmPackage:str ):
        Thread.__init__(self)
        self.gui = app2Update
        self.packageName =npmPackage


    def run(self):
        npmInfoClient = NpmWrapper()
        dataToShow = npmInfoClient.getPackageGeneralInfo(self.packageName)
        if not dataToShow:
            self.gui.after(0,self.gui.showPopuError())
        else:
            self.gui.after(0, self.gui.updateGeneralInfoTab(dataToShow))
            now = datetime.now()
            createdAt = datetime.strptime(dataToShow.createdDate,"%d/%m/%Y")

            nbTotalDownload = 0
            listInterval =NpmWrapper.getListIntervalOneYearNpm(createdAt,now)
            for interval in listInterval:
                downloadTmp = npmInfoClient.getDownloadBetween2Date(dataToShow.name,interval.get("start"), interval.get("end"))
                if downloadTmp:
                    nbTotalDownload += sum(downloadTmp.downloads)

            # get last 7 days graph
            listDownloads = npmInfoClient.getLast7daysDownload(dataToShow.name)

            self.gui.after(0, self.gui.updateDownloadInfoTab(dataToShow,nbTotalDownload,listDownloads))
        

if __name__ == "__main__":
	app = MyApp()
	app.mainloop()