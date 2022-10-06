from tkinter import *
from tkinter import ttk, filedialog, Toplevel
from NpmHelper import NpmWrapper


class InfoPackage(Toplevel):

    def __init__(self,parent, packageName:str):
        Toplevel.__init__(self, parent)

        self.title("Infos pour " + packageName)

        self.mainframe = ttk.Frame(self, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # retour etat traitement
        self.infoError = StringVar()
        ttk.Label(self.mainframe, textvariable=self.infoError).grid(column=1, row=0, sticky=(W, E))

        npmInfoClient = NpmWrapper()
        dataToShow = npmInfoClient.getPackageGeneralInfo(packageName)

        if not dataToShow:
            self.infoError.set("Impossible de trouver des infos sur " + packageName)
        
        else:
            ttk.Label(self.mainframe,text="Nom: " + dataToShow.name).grid(column=0, row=0, sticky=(W, E))
            ttk.Label(self.mainframe,text="Description: " + dataToShow.description).grid(column=0, row=1, sticky=(W, E))
            ttk.Label(self.mainframe,text="Dernière version: " + dataToShow.version).grid(column=0, row=2, sticky=(W, E))
            ttk.Label(self.mainframe,text="Auteur: " + dataToShow.author).grid(column=0, row=3, sticky=(W, E))
        
            ttk.Labelframe(self.mainframe,text="README").grid(column=0, row=5, sticky=(W, E))

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)


        # Gets the requested values of the height and width.
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        self.positionRight = int(self.winfo_screenwidth()/2 - windowWidth/2)
        self.positionDown = int(self.winfo_screenheight()/2 - windowHeight/2)

    
    #def getfilename(self):
    #    filename =  filedialog.askopenfilename(initialdir = "./",title = "Selectionner un fichier",filetypes = (("csv files","*.csv"),("tous les fichiers","*.*")))
    #    print (filename)
    #    self.myPath.set(filename)


    def suppression(self, popup:Toplevel):
        popup.destroy()