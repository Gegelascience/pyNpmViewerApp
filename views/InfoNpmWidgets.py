from tkinter import *
from tkinter import ttk
from Helpers.NpmHelper import PackageDataInfo

class InfoPackageWidget(Frame):

    def __init__(self,parent, packageInfo:PackageDataInfo):
        Frame.__init__(self, parent)

        
        ttk.Label(self,text= packageInfo.name).pack(pady=(20,0))

        generalDataContainer = Frame(self)

        generalDataFrameLeft =Frame(generalDataContainer)
        columnLabel = Frame(generalDataFrameLeft)

        ttk.Label(columnLabel,text="Auteur: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Date de création: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Dernière version: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Licence: ").pack(anchor="w")

        columnValue = Frame(generalDataFrameLeft)
        ttk.Label(columnValue,text=packageInfo.author).pack(anchor="w")
        ttk.Label(columnValue,text=packageInfo.createdDate).pack(anchor="w")
        ttk.Label(columnValue,text=packageInfo.version).pack(anchor="w")
        ttk.Label(columnValue,text=packageInfo.license).pack(anchor="w")
        
        columnLabel.pack(side=LEFT)
        columnValue.pack()
        generalDataFrameLeft.pack(side=LEFT)


        generalDataFrameRight = Frame(generalDataContainer)
        ttk.Label(generalDataFrameRight,text="Description: ").pack()
        ttk.Label(generalDataFrameRight,text=packageInfo.description).pack()
        ttk.Label(generalDataFrameRight,text="Mots clés: ").pack()
        ttk.Label(generalDataFrameRight,text=packageInfo.keywords).pack()

        generalDataFrameRight.pack()

        generalDataContainer.pack()




        scrollbarReadme=Scrollbar(self,orient="vertical")
        scrollbarReadme.pack(side="right",fill="y")

        readmeLinesContainer = Text(self,yscrollcommand=scrollbarReadme.set, height=200)
            
        for line in packageInfo.readmeLines:
            readmeLinesContainer.insert(END,"\r\n"+line)

        readmeLinesContainer.pack(side = LEFT, fill = BOTH )

        scrollbarReadme.config( command = readmeLinesContainer.yview )


class GraphDownloadsWidget(Frame):
    def __init__(self,parent, packageInfo:PackageDataInfo,nbTotalDownload,listDownloads:list):
        Frame.__init__(self, parent)

        # retour etat traitement
        self.infoError = StringVar()
        ttk.Label(self, textvariable=self.infoError).pack()

        ttk.Label(self,text="Nom: " + packageInfo.name).pack()

        ttk.Label(self,text="Total: " + str(nbTotalDownload)).pack(pady=(0,50))


        
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

            

