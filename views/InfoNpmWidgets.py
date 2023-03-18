from tkinter import *
from tkinter import ttk,filedialog
from Helpers.NpmHelper import PackageDataInfo
import webbrowser
import csv
from Helpers.SvgHelper import saveGraphAsSvg

from models.NpmModels import PackageDownloadInfo

class InfoPackageWidget(Frame):
    """
    Frame to display general information on package
    """
    data:PackageDataInfo

    def __init__(self,parent, packageInfo:PackageDataInfo):
        super().__init__(parent)

        # fenetre fond blanc
        self.configure(bg='white')

        self.data = packageInfo
        
        ttk.Label(self,text= self.data.name).pack(pady=(20,0))

        generalDataContainer = Frame(self)

        columnLabel = Frame(generalDataContainer,background="white")

        ttk.Label(columnLabel,text="Auteur: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Date de création: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Dernière version: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Licence: ").pack(anchor="w")

        ttk.Label(columnLabel,text="Description: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Mots clés: ").pack(anchor="w")

        columnValue = Frame(generalDataContainer,background="white")
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
        """
        Open npm package page on default browser
        """
        webbrowser.open_new_tab("https://www.npmjs.com/package/" + self.data.name)


class ReadMeViewerWidget(Frame):
    """
    Frame to display package readme content
    """

    def __init__(self,parent,packageInfo:PackageDataInfo):
        super().__init__(parent)

        # fenetre fond blanc
        self.configure(bg='white')

        ttk.Label(self,text= packageInfo.name).pack(pady=(20,0))

        scrollbarReadme=Scrollbar(self,orient="vertical")
        scrollbarReadme.pack(side="right",fill="y")

        readmeLinesContainer = Text(self,yscrollcommand=scrollbarReadme.set, height=200)
            
        for line in packageInfo.readmeLines:
            readmeLinesContainer.insert(END,"\r\n"+line)

        readmeLinesContainer.pack(side = LEFT, fill = BOTH )

        scrollbarReadme.config( command = readmeLinesContainer.yview)


class GraphDownloadsWidget(Frame):
    """
    Frame to display package download informations
    """
    listData:list
    last30days:PackageDownloadInfo
    
    def __init__(self,parent, packageInfo:PackageDataInfo,nbTotalDownload,listDownloadsSeven:PackageDownloadInfo, listDownloadsThirty:PackageDownloadInfo):
        super().__init__(parent)

        # fenetre fond blanc
        self.configure(bg='white')

        # retour etat traitement
        self.infoError = StringVar()
        ttk.Label(self, textvariable=self.infoError).pack()

        ttk.Label(self,text="Nom: " + packageInfo.name).pack()
        ttk.Label(self,text="Total: " + str(nbTotalDownload)).pack(pady=(0,50))

        
        if not listDownloadsSeven and not listDownloadsThirty:
            self.infoError.set("Impossible de trouver des infos sur " + packageInfo.name)
        
        if listDownloadsSeven:
            self.drawDownloadGraph(listDownloadsSeven,51,"7 derniers jours",(0,50))

        if listDownloadsThirty:
            self.drawDownloadGraph(listDownloadsThirty,14,"30 derniers jours")
            self.listData = [{"Téléchagements":d} for d in listDownloadsThirty.downloads]
            self.last30days = listDownloadsThirty

            btnReport = ttk.Button(self, text="Exporter", command=self.exportDownloadReport)
            btnReport.bind('<Return>', self.exportDownloadReport)
            btnReport.pack(pady=(10,0))
        

    def drawDownloadGraph(self,listDownload:PackageDownloadInfo, interValueSpace:int, graphTitle:str, padding:tuple=(0,0)):
        """
        Draw a graph to represent download evolution
        """
        maxValue = max(listDownload.downloads)
        minValue = min(listDownload.downloads)

        ttk.Label(self,text=graphTitle).pack()
        graph = Canvas(self,height=120,width=425, background="white")
        graph.pack(fill=X,pady=padding)
            
        for i,dayStat in enumerate(listDownload.downloads):
            if dayStat in (minValue,maxValue):
                graph.create_text(i*interValueSpace + 5,10,text=dayStat)
            if i > 0:
                graph.create_line((i-1)*interValueSpace + 5, 20+(maxValue-listDownload.downloads[i-1])*100/maxValue, i*interValueSpace + 5, 20+(maxValue-dayStat)*100/maxValue,width=3, fill="red")


    def exportDownloadReport(self):
        """
        Export package download informations as csv 
        """
        targetFilename = filedialog.asksaveasfilename(filetypes=[("csv file","*.csv")], defaultextension=".csv",initialfile="downloadNpm.csv", title="Télécharger le rapport")
        if targetFilename:
            with open(targetFilename,mode="w", encoding='utf-8',newline='') as report:
                dictWriter = csv.DictWriter(report,fieldnames=["Téléchagements"])
                dictWriter.writeheader()
                for row in self.listData:
                    dictWriter.writerow(row)
            
            saveGraphAsSvg(self.last30days,targetFilename.replace(".csv",".svg"))

