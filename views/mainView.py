from tkinter import Tk, ttk
from tkinter import *
from views.InfoNpmWidgets import InfoPackageWidget,GraphDownloadsWidget
from controllers.DataNpmController import GetNpmDataThread



class MyApp(Tk):

    def __init__(self):
        super().__init__()
        
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
        if len(packageName) > 0 :
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
        super().__init__(parent)
        self.title("ERREUR")
        self.geometry('150x50')
        ttk.Label(self,text="Une erreur est survenue").pack()