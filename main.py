from tkinter import Tk, ttk
from tkinter import *
from InfoNpmWidgets import InfoPackageWidget,GraphDownloadsWidget
from NpmHelper import NpmWrapper

class myApp(Tk):

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

        npmInfoClient = NpmWrapper()
        dataToShow = npmInfoClient.getPackageGeneralInfo(packageName)
        if not dataToShow:
            ErrorPopup(self)
        else:
            for child in self.tabInfo.winfo_children():
                child.destroy()
            InfoPackageWidget(self.tabInfo, dataToShow).pack()

            for child in self.tabDownload.winfo_children():
                child.destroy()
            GraphDownloadsWidget(self.tabDownload, dataToShow).pack()


class ErrorPopup(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("ERREUR")
        self.geometry('150x50')
        ttk.Label(self,text="Une erreur est survenue").pack()

	

if __name__ == "__main__":
	app = myApp()
	app.mainloop()