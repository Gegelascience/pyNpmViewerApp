from tkinter import *
from tkinter import ttk,filedialog
from Helpers.NpmHelper import PackageDataInfo
import webbrowser
import csv
from Helpers.ChartHelper import LineChartWrapper
from models.NpmModels import PackageDownloadInfo
from Helpers.ConfigurationFileParser import ConfigurationFileData

class InfoPackageWidget(Frame):
    """
    Frame to display general information on package
    """
    data:PackageDataInfo

    def __init__(self,parent, packageInfo:PackageDataInfo):
        super().__init__(parent)

        # fenetre fond blanc
        myConfigParser = ConfigurationFileData("config.properties","dev")
        self.configure(bg=myConfigParser.getconfkey("color.secondary"))

        self.data = packageInfo
        
        ttk.Label(self,text= self.data.name).pack(pady=(20,10))

        generalDataContainer = Frame(self,background=myConfigParser.getconfkey("color.secondary"))

        columnLabel = Frame(generalDataContainer,background=myConfigParser.getconfkey("color.secondary"))

        ttk.Label(columnLabel,text="Contributeurs: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Date de création: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Dernière version: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Licence: ").pack(anchor="w")

        ttk.Label(columnLabel,text="Description: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Mots clés: ").pack(anchor="w")
        ttk.Label(columnLabel,text="Integrité \n(dernière version): ").pack(anchor="w")

        columnValue = Frame(generalDataContainer,background=myConfigParser.getconfkey("color.secondary"))
        ttk.Label(columnValue,text=self.data.contributors).pack(anchor="w")
        ttk.Label(columnValue,text=self.data.createdDate).pack(anchor="w")
        ttk.Label(columnValue,text=self.data.version).pack(anchor="w")
        ttk.Label(columnValue,text=self.data.license).pack(anchor="w")
        
        ttk.Label(columnValue,text=self.data.description).pack(anchor="w")
        ttk.Label(columnValue,text=self.data.keywords).pack(anchor="w")

        if self.data.lastVersionIntegrity:
            ttk.Label(columnValue,text="\nOK").pack(anchor="w")
        else:
            ttk.Label(columnValue,text="\nKO").pack(anchor="w")
        
        columnLabel.pack(side=LEFT)
        columnValue.pack()

        generalDataContainer.pack()

        btnAccesNpmPage = ttk.Button(self, text="Accès page npm", command=self.openNpmPage)
        btnAccesNpmPage.bind('<Return>', self.openNpmPage)
        btnAccesNpmPage.pack(pady=(10,0))

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
        myConfigParser = ConfigurationFileData("config.properties","dev")
        self.configure(bg=myConfigParser.getconfkey("color.secondary"))

        ttk.Label(self,text= packageInfo.name).pack(pady=(20,10))

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
    
    def __init__(self,parent, packageInfo:PackageDataInfo,nbTotalDownload,listDownloadsSeven:PackageDownloadInfo, listDownloadsThirty:PackageDownloadInfo):
        super().__init__(parent)

        # fenetre fond blanc
        myConfigParser = ConfigurationFileData("config.properties","dev")
        self.configure(bg=myConfigParser.getconfkey("color.secondary"))

        # retour etat traitement
        self.infoError = StringVar()
        ttk.Label(self, textvariable=self.infoError).pack()

        ttk.Label(self,text="Nom: " + packageInfo.name).pack()
        ttk.Label(self,text="Total: " + str(nbTotalDownload)).pack(pady=(0,50))

        
        if not listDownloadsSeven and not listDownloadsThirty:
            self.infoError.set("Impossible de trouver des infos sur " + packageInfo.name)

        primaryColor =myConfigParser.getconfkey("color.primary")
        secondaryColor =myConfigParser.getconfkey("color.secondary")
        
        if listDownloadsSeven:
            self.lineChartSeven = LineChartWrapper(listDownloadsSeven.downloads)
            self.lineChartSeven.drawCanvas("7 derniers jours",self,51,primaryColor, secondaryColor,(0,50))

        if listDownloadsThirty:
            self.lineChart30 = LineChartWrapper(listDownloadsThirty.downloads)
            self.lineChart30.drawCanvas("30 derniers jours",self,14,primaryColor, secondaryColor)

            self.listData = [{"Jour":listDownloadsThirty.days[i],"Téléchagements":download} for i,download in enumerate(listDownloadsThirty.downloads)]

            btnReport = ttk.Button(self, text="Exporter", command=self.exportDownloadReport)
            btnReport.bind('<Return>', self.exportDownloadReport)
            btnReport.pack(pady=(10,0))


    def exportDownloadReport(self):
        """
        Export package download informations as csv 
        """
        targetFilename = filedialog.asksaveasfilename(filetypes=[("csv file","*.csv")], defaultextension=".csv",initialfile="downloadNpm.csv", title="Télécharger le rapport")
        if targetFilename:
            with open(targetFilename,mode="w", encoding='utf-8',newline='') as report:
                dictWriter = csv.DictWriter(report,fieldnames=["Jour","Téléchagements"])
                dictWriter.writeheader()
                for row in self.listData:
                    dictWriter.writerow(row)

            self.lineChart30.saveAsSvg(targetFilename.replace(".csv",".svg"))

