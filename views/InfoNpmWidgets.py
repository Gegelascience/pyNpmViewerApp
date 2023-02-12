from tkinter import *
from tkinter import ttk
from Helpers.NpmHelper import PackageDataInfo
import webbrowser

class InfoPackageWidget(Frame):
    data:PackageDataInfo

    def __init__(self,parent, packageInfo:PackageDataInfo):
        super().__init__(parent)

        self.data = packageInfo
        
        ttk.Label(self,text= self.data.name).pack(pady=(20,0))

        generalDataContainer = Frame(self)

        columnLabel = Frame(generalDataContainer)

        ttk.Label(columnLabel,text="Auteur: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Date de création: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Dernière version: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Licence: ").pack(anchor="w")

        ttk.Label(columnLabel,text="Description: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Mots clés: ").pack(anchor="w")

        columnValue = Frame(generalDataContainer)
        ttk.Label(columnValue,text=self.data.author).pack(anchor="w")
        ttk.Label(columnValue,text=self.data.createdDate).pack(anchor="w")
        ttk.Label(columnValue,text=self.data.version).pack(anchor="w")
        ttk.Label(columnValue,text=self.data.license).pack(anchor="w")
        
        ttk.Label(columnValue,text=self.data.description).pack(anchor="w")
        ttk.Label(columnValue,text=self.data.keywords).pack(anchor="w")
        
        columnLabel.pack(side=LEFT)
        columnValue.pack()

        generalDataContainer.pack()

        btnAccesNpmPage = ttk.Button(self, text="Accès page npm", command=self.openNpmPage)
        btnAccesNpmPage.bind('<Return>', self.openNpmPage)
        btnAccesNpmPage.pack()

    def openNpmPage(self):
        webbrowser.open_new_tab("https://www.npmjs.com/package/" + self.data.name)


class ReadMeViewerWidget(Frame):

    def __init__(self,parent,packageInfo:PackageDataInfo):
        super().__init__(parent)

        ttk.Label(self,text= packageInfo.name).pack(pady=(20,0))

        scrollbarReadme=Scrollbar(self,orient="vertical")
        scrollbarReadme.pack(side="right",fill="y")

        readmeLinesContainer = Text(self,yscrollcommand=scrollbarReadme.set, height=200)
            
        for line in packageInfo.readmeLines:
            readmeLinesContainer.insert(END,"\r\n"+line)

        readmeLinesContainer.pack(side = LEFT, fill = BOTH )

        scrollbarReadme.config( command = readmeLinesContainer.yview)


class GraphDownloadsWidget(Frame):
    def __init__(self,parent, packageInfo:PackageDataInfo,nbTotalDownload,listDownloadsSeven:list, listDownloadsThirty:list):
        super().__init__(parent)

        # retour etat traitement
        self.infoError = StringVar()
        ttk.Label(self, textvariable=self.infoError).pack()

        ttk.Label(self,text="Nom: " + packageInfo.name).pack()

        ttk.Label(self,text="Total: " + str(nbTotalDownload)).pack(pady=(0,50))


        
        if not listDownloadsSeven and not listDownloadsThirty:
            self.infoError.set("Impossible de trouver des infos sur " + packageInfo.name)
        
        if listDownloadsSeven:
            maxValue = max(listDownloadsSeven.downloads)

            ttk.Label(self,text="7 derniers jours").pack()
            graph = Canvas(self,height=120,width=425, background="white")
            graph.pack(fill=X,pady=(0,50))
            
            for i,dayStat in enumerate(listDownloadsSeven.downloads):
                graph.create_text(i*51 + 5,10,text=dayStat)
                if i > 0:
                    graph.create_line((i-1)*51 + 5, 20+(maxValue-listDownloadsSeven.downloads[i-1])*100/maxValue, i*51 + 5, 20+(maxValue-dayStat)*100/maxValue,width=3, fill="red")


        if listDownloadsThirty:
            maxValue = max(listDownloadsThirty.downloads)

            ttk.Label(self,text="30 derniers jours").pack()
            graph = Canvas(self,height=120,width=425, background="white")
            graph.pack(fill=X)
            
            for i,dayStat in enumerate(listDownloadsThirty.downloads):
                graph.create_text(i*14 + 5,10,text=dayStat)
                if i > 0:
                    graph.create_line((i-1)*14 + 5, 20+(maxValue-listDownloadsThirty.downloads[i-1])*100/maxValue, i*14 + 5, 20+(maxValue-dayStat)*100/maxValue,width=3, fill="red")
            

