from tkinter import Tk, ttk, PhotoImage
from tkinter import *
from views.InfoNpmWidgets import InfoPackageWidget,GraphDownloadsWidget,ReadMeViewerWidget
from controllers.DataNpmController import GetNpmDataThread
from views.genericWidgets import ErrorPopup, LoaderFrame
from Helpers.PngHelper import PngBuilder

def addLoader(parentFrame: Frame):
	"""
	Add a loader Frame to a parent Frame
	"""
	for child in parentFrame.winfo_children():
		child.destroy()
	LoaderFrame(parentFrame).pack()

def generateIconImg() -> PhotoImage:
	actualData = []

	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			if row > 2 and row <29 and (col in [4,5,6,25,26,27] or col==row or col == row+1 or col == row-1):

				rowData.append([255,255,255,255])
			else:
				rowData.append([255,0,0,255])
			col+=1
		actualData.append(rowData)	
		row+=1

	pngBuilder = PngBuilder(actualData,32,32)
	return PhotoImage(data= pngBuilder.binaryContent)

class MyApp(Tk):
	"""
	App Class
	"""

	def __init__(self):
		super().__init__()
		
		self.title("Informations Package NPM")
		self.geometry('600x800')

		# fenetre fond blanc
		self.configure(bg='white')

		# Create an instance of ttk style
		s = ttk.Style()
		s.theme_use('default')
		s.configure('TNotebook.Tab', background="white")
		s.map("TNotebook.Tab", background= [("selected", "red")])
		s.map("TNotebook.Tab", foreground= [("selected", "white")])

		s.configure('TNotebook', background="white")
		s.configure('TFrame', background="white")
		s.configure('TLabel', background="white")
		s.configure("TButton", background="red", foreground="white",pady=10)


		# customisation de l'icone
		photo = generateIconImg()
		self.wm_iconphoto(True,photo)

		ttk.Label(self,text="Renseignez le nom du package").pack(pady=(5,0))
		
		# ajout du champ formulaire
		self.package = StringVar()
		package_entry = ttk.Entry(self, width=20, textvariable=self.package)
		package_entry.pack(pady=(10,0))
		
		btnSearch = ttk.Button(self, text="Rechercher", command=self.showInformation)
		btnSearch.bind('<Return>', self.showInformation)
		btnSearch.pack(pady=(10,0))

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

	def showPopupError(self, message):
		"""
		Show error popup
		"""
		ErrorPopup(self, message)


if __name__ == "__main__":
	app = MyApp()
	app.mainloop()
		


