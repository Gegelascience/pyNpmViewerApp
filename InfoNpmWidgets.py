from tkinter import *
from tkinter import ttk
from NpmHelper import NpmWrapper, PackageDataInfo
from datetime import datetime


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


class InfoPackageWidget(Frame):

    def __init__(self,parent, packageInfo:PackageDataInfo):
        Frame.__init__(self, parent)

        ttk.Label(self,text="Nom: " + packageInfo.name).pack()
        ttk.Label(self,text="Description: " + packageInfo.description).pack()
        ttk.Label(self,text="Mots clés: " + packageInfo.keywords).pack()
        ttk.Label(self,text="Auteur: " + packageInfo.author).pack()
        ttk.Label(self,text="Dernière version: " + packageInfo.version).pack()
        ttk.Label(self,text="Date de création: " + packageInfo.createdDate).pack()
        ttk.Label(self,text="Licence: " + packageInfo.license).pack()
            

        scrollbarReadme=Scrollbar(self,orient="vertical")
        scrollbarReadme.pack(side="right",fill="y")

        readmeLinesContainer = Text(self,yscrollcommand=scrollbarReadme.set, height=200)
            
        for line in packageInfo.readmeLines:
            readmeLinesContainer.insert(END,"\r\n"+line)

        readmeLinesContainer.pack(side = LEFT, fill = BOTH )

        scrollbarReadme.config( command = readmeLinesContainer.yview )


class GraphDownloadsWidget(Frame):
    def __init__(self,parent, packageInfo:PackageDataInfo):
        Frame.__init__(self, parent)

        # retour etat traitement
        self.infoError = StringVar()
        ttk.Label(self, textvariable=self.infoError).pack()

        ttk.Label(self,text="Nom: " + packageInfo.name).pack()


        nbTotalDownload = 0

        npmInfoClient = NpmWrapper()

        now = datetime.now()
        createdAt = datetime.strptime(packageInfo.createdDate,"%d/%m/%Y")

        listInterval =getListIntervalOneYearNpm(createdAt,now)
        downloadByYear = []
        for interval in listInterval:
            downloadTmp = npmInfoClient.getDownloadBetween2Date(packageInfo.name,interval.get("start"), interval.get("end"))
            if downloadTmp:
                nbTotalDownload += sum(downloadTmp.downloads)


        ttk.Label(self,text="Total: " + str(nbTotalDownload)).pack()


        # get last 7 days graph
        listDownloads = npmInfoClient.getLast7daysDownload(packageInfo.name)
        if not listDownloads:
            self.infoError.set("Impossible de trouver des infos sur " + packageInfo.name)
        else:

            maxValue = max(listDownloads.downloads)

            ttk.Label(self,text="7 derniers jours").pack()
            graph = Canvas(self,height=120,width=400, background="white")
            graph.pack(side=LEFT,fill=X)
            
            for i,dayStat in enumerate(listDownloads.downloads):
                graph.create_text(i*50 + 5,10,text=dayStat)
                graph.create_line(i*50 + 5, 20+(maxValue-dayStat)*100/maxValue, i*50 + 5, 120,width=3, fill="red")

            

