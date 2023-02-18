from tkinter import Tk, ttk
from tkinter import *
from views.InfoNpmWidgets import InfoPackageWidget,GraphDownloadsWidget,ReadMeViewerWidget
from controllers.DataNpmController import GetNpmDataThread
from views.genericWidgets import ErrorPopup, LoaderFrame

def addLoader(parentFrame: Frame):
    """
    Add a loader Frame to a parent Frame
    """
    for child in parentFrame.winfo_children():
        child.destroy()
    LoaderFrame(parentFrame).pack()

class MyApp(Tk):
    """
    App Class
    """

    def __init__(self):
        super().__init__()
        
        self.title("Informations Package NPM")
        self.geometry('600x800')

        ttk.Label(self,text="Renseigner le nom du package").pack()
        
        # ajout du champ formulaire
        self.package = StringVar()
        package_entry = ttk.Entry(self, width=20, textvariable=self.package)
        package_entry.pack()
        
        btnSearch = ttk.Button(self, text="Rechercher", command=self.showInformation)
        btnSearch.bind('<Return>', self.showInformation)
        btnSearch.pack()

        tabControl = ttk.Notebook(self)
  
        self.tabInfo = ttk.Frame(tabControl)
        self.tabReadMe = ttk.Frame(tabControl)
        self.tabDownload = ttk.Frame(tabControl)

        tabControl.add(self.tabInfo, text ='Informations')
        tabControl.add(self.tabReadMe, text ='ReadMe')
        tabControl.add(self.tabDownload, text ='Téléchargements')
        tabControl.pack(expand = 1, fill ="both")

        package_entry.focus()

    def showInformation(self, event=None):
        packageName = self.package.get()
        if len(packageName) > 0 :
            npmThread = GetNpmDataThread(self,packageName)
            addLoader(self.tabInfo)
            addLoader(self.tabReadMe)
            addLoader(self.tabDownload)
            npmThread.start()

    def updateGeneralInfoTab(self, dataFromNpm):
        for child in self.tabInfo.winfo_children():
            child.destroy()
        InfoPackageWidget(self.tabInfo, dataFromNpm).pack()
        for child in self.tabReadMe.winfo_children():
            child.destroy()
        ReadMeViewerWidget(self.tabReadMe, dataFromNpm).pack()

    def updateDownloadInfoTab(self, generalDataFromNpm, sumDownload, lastSevenDays,listDownloadsThirty):
        """
        Show tab with package download informations
        """
        for child in self.tabDownload.winfo_children():
            child.destroy()
        GraphDownloadsWidget(self.tabDownload, generalDataFromNpm, sumDownload,lastSevenDays,listDownloadsThirty).pack()	

    def showPopupError(self):
        """
        Show error popup
        """
        ErrorPopup(self)

        


