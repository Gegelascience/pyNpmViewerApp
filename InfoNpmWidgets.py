from tkinter import *
from tkinter import ttk, Toplevel
from NpmHelper import NpmWrapper


class InfoPackageWidget(Frame):

    def __init__(self,parent, packageName:str):
        Frame.__init__(self, parent)

        # retour etat traitement
        self.infoError = StringVar()
        ttk.Label(self, textvariable=self.infoError).pack()

        npmInfoClient = NpmWrapper()
        dataToShow = npmInfoClient.getPackageGeneralInfo(packageName)

        if not dataToShow:
            self.infoError.set("Impossible de trouver des infos sur " + packageName)
        
        else:
            ttk.Label(self,text="Nom: " + dataToShow.name).pack()
            ttk.Label(self,text="Description: " + dataToShow.description).pack()
            ttk.Label(self,text="Mots clés: " + dataToShow.keywords).pack()
            ttk.Label(self,text="Auteur: " + dataToShow.author).pack()
            ttk.Label(self,text="Dernière version: " + dataToShow.version).pack()
            ttk.Label(self,text="Licence: " + dataToShow.license).pack()
            

            scrollbarReadme=Scrollbar(self,orient="vertical")
            scrollbarReadme.pack(side="right",fill="y")

            readmeLinesContainer = Text(self,yscrollcommand=scrollbarReadme.set, height=200)
            
            for line in dataToShow.readmeLines:
                readmeLinesContainer.insert(END,"\r\n"+line)

            readmeLinesContainer.pack(side = LEFT, fill = BOTH )

            scrollbarReadme.config( command = readmeLinesContainer.yview )


class GraphDownloadsWidget(Frame):
    def __init__(self,parent, packageName:str):
        Frame.__init__(self, parent)

        # retour etat traitement
        self.infoError = StringVar()
        ttk.Label(self, textvariable=self.infoError).pack()

        npmInfoClient = NpmWrapper()
        listDownloads = npmInfoClient.getLast7daysDownload(packageName)
        if not listDownloads:
            self.infoError.set("Impossible de trouver des infos sur " + packageName)
        else:
            ttk.Label(self,text="Nom: " + listDownloads.name).pack()

            maxValue = max(listDownloads.downloads)

            ttk.Label(self,text="7 derniers jours").pack()
            graph = Canvas(self,height=120,width=400, background="white")
            graph.pack(side=LEFT,fill=X)
            
            for i,dayStat in enumerate(listDownloads.downloads):
                graph.create_text(i*50 + 5,10,text=dayStat)
                graph.create_line(i*50 + 5, 20+(maxValue-dayStat)*100/maxValue, i*50 + 5, 120,width=3, fill="red")

            

