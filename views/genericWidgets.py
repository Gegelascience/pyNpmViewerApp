from tkinter import Tk, ttk
from tkinter import *


class ErrorPopup(Toplevel):
    """
    Popup d'erreur
    """
    def __init__(self, parent, textError:str="Une erreur est survenue"):
        super().__init__(parent)
        self.title("ERREUR")
        self.geometry('150x50')

        # fenetre fond blanc
        self.configure(bg='white')

        ttk.Label(self,text=textError).pack(pady=(20,0))
        


class LoaderFrame(Frame):
    """
    Loader Animation Frame
    """
    loaderIconCanvas:Canvas

    def __init__(self,parent:Frame):
        super().__init__(parent)

        # fenetre fond blanc
        self.configure(bg='white')

        self.zoneLoader = 0
        ttk.Label(self,text="Récupération en cours").pack(pady=(20,10))

        self.loaderIconCanvas = Canvas(self, width=150, height=100)

        self.loaderIconCanvas.configure(bg="white",highlightthickness=0)

        self.loaderIconCanvas.pack()

        self.updateLoader()
        


    def updateLoader(self,item=None):
        """
        Update loader animation
        """
        self.loaderIconCanvas.delete(item)
        xPoint=(self.zoneLoader%3)*50
        yPoint=0
        length=50

        item=self.loaderIconCanvas.create_rectangle(xPoint, yPoint, xPoint+length, yPoint+length, fill='red', outline='')
        self.zoneLoader+=1

        self.after(500, self.updateLoader,item)
