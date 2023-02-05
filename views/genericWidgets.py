from tkinter import Tk, ttk
from tkinter import *
from random import randint


class ErrorPopup(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("ERREUR")
        self.geometry('150x50')
        ttk.Label(self,text="Une erreur est survenue").pack()


class LoaderFrame(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.zoneLoader = 0
        ttk.Label(self,text="Récupération en cours").pack(pady=(20,0))

        self.loaderIcon = Canvas(self, width=150, height=100)
        self.loaderIcon.pack()

        self.updateLoader()
        


    def updateLoader(self,item=None):
        self.loaderIcon.delete(item)
        xPoint=(self.zoneLoader%3)*50
        yPoint=0
        length=50

        item=self.loaderIcon.create_rectangle(xPoint, yPoint, xPoint+length, yPoint+length, fill='red', outline='')
        self.zoneLoader+=1

        self.after(1000, self.updateLoader,item)
