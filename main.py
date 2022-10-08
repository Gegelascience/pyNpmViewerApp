from tkinter import Tk, ttk
from tkinter import *
from InfoNpmWidgets import InfoPackageWidget,GraphDownloadsWidget


class myApp(Tk):



    def __init__(self):
        Tk.__init__(self)
        self.title("Npm package Informations")

        self.geometry('600x800')

        ttk.Label(self,text="Renseigner le nom du package").pack()
        
        # ajout du champ formulaire
        self.package = StringVar()
        package_entry = ttk.Entry(self, width=20, textvariable=self.package)
        package_entry.pack()
        
        ttk.Button(self, text="Rechercher", command=self.openInformationPopup).pack()


        tabControl = ttk.Notebook(self)
  
        self.tabInfo = ttk.Frame(tabControl)
        self.tabDownload = ttk.Frame(tabControl)

        tabControl.add(self.tabInfo, text ='Informations')
        tabControl.add(self.tabDownload, text ='Téléchargement')
        tabControl.pack(expand = 1, fill ="both")

        package_entry.focus()

    def openInformationPopup(self):
        packageName = self.package.get()
        for child in self.tabInfo.winfo_children():
            child.destroy()
        InfoPackageWidget(self.tabInfo, packageName).pack()

        for child in self.tabDownload.winfo_children():
            child.destroy()
        GraphDownloadsWidget(self.tabDownload, packageName).pack()



	

if __name__ == "__main__":
	app = myApp()
	app.mainloop()