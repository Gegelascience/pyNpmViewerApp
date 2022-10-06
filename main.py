from tkinter import Tk, ttk
from tkinter import *
from InfoPopup import InfoPackage


class myApp(Tk):



    def __init__(self):
        Tk.__init__(self)
        self.title("Npm package Informations")

        self.geometry('600x100')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # ajout du champ formulaire
        self.user = StringVar()
        user_entry = ttk.Entry(self, width=20, textvariable=self.user)
        user_entry.grid(
            column=1,
            row=0)

        ttk.Label(self,text="Renseigner le nom du package").grid(
            column=0,
            row=0)

        ttk.Button(self, text="Rechercher", command=self.openInformationPopup).grid(
            column=2,
            row=0)


    def openInformationPopup(self):
        packageName = self.user.get()
        InfoPackage(self, packageName)


	

if __name__ == "__main__":
	app = myApp()
	app.mainloop()