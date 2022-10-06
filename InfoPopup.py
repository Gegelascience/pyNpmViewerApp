from tkinter import *
from tkinter import ttk, filedialog, Toplevel
from NpmHelper import NpmWrapper


class InfoPackage(Toplevel):

    def __init__(self,parent, packageName:str):
        Toplevel.__init__(self, parent)

        self.title("Infos pour " + packageName)

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
            
            readmeZone =ttk.Labelframe(self,text="README").pack(fill="both", expand="yes")
            for line in dataToShow.readmeLines:
                ttk.Label(readmeZone, text=line).pack()


    
    #def getfilename(self):
    #    filename =  filedialog.askopenfilename(initialdir = "./",title = "Selectionner un fichier",filetypes = (("csv files","*.csv"),("tous les fichiers","*.*")))
    #    print (filename)
    #    self.myPath.set(filename)


    def suppression(self, popup:Toplevel):
        popup.destroy()