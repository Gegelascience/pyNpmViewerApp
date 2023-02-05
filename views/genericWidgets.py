from tkinter import Tk, ttk
from tkinter import *


class ErrorPopup(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("ERREUR")
        self.geometry('150x50')
        ttk.Label(self,text="Une erreur est survenue").pack()


class LoaderFrame(Frame):
    def __init__(self,parent):
        super().__init__(parent)
        ttk.Label(self,text="Récupération en cours").pack(fill="both")