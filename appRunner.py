from tkinter import Tk, ttk, PhotoImage, Frame, StringVar
from views.InfoNpmWidgets import InfoPackageWidget,GraphDownloadsWidget,ReadMeViewerWidget
from controllers.DataNpmController import GetNpmDataThread
from views.genericWidgets import ErrorPopup, LoaderFrame
from appHelpers.PngHelper import PngBuilder
from appHelpers.ConfigurationFileParser import ConfigurationFileData
from models.GuiModels import UIOptions


def getGUIOptions(configFilePath:str, section:str):
	try:
		myConfigParser = ConfigurationFileData(configFilePath,section)
		myOptions = UIOptions()

		if myConfigParser.getconfkey("window.main.size"):
			myOptions.windowMainSize =myConfigParser.getconfkey("window.main.size")
		if myConfigParser.getconfkey("window.popin.size"):
			myOptions.windowPopinSize = myConfigParser.getconfkey("window.popin.size")
		if myConfigParser.getconfkey("color.primary"):
			myOptions.colorPrimary = myConfigParser.getconfkey("color.primary")
		if myConfigParser.getconfkey("window.popin.size"):
			myOptions.colorSecondary = myConfigParser.getconfkey("color.secondary")
		
		return myOptions
	except:
		return UIOptions()

def addLoader(parentFrame: Frame, options:UIOptions):
	"""
	Add a loader Frame to a parent Frame
	"""
	for child in parentFrame.winfo_children():
		child.destroy()
	LoaderFrame(parentFrame,options).pack()

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

	def __init__(self, options:UIOptions):
		super().__init__()
		
		self.title("Informations Package NPM")

		self.options =options

		self.geometry(self.options.windowMainSize)

		# fenetre fond blanc
		self.configure(bg=self.options.colorSecondary)

		# Create an instance of ttk style
		s = ttk.Style()
		s.theme_use('default')
		s.configure('TNotebook.Tab', background=self.options.colorSecondary)
		s.map("TNotebook.Tab", background= [("selected", self.options.colorPrimary)])
		s.map("TNotebook.Tab", foreground= [("selected", self.options.colorSecondary)])

		s.configure('TNotebook', background=self.options.colorSecondary)
		s.configure('TFrame', background=self.options.colorSecondary)
		s.configure('TLabel', background=self.options.colorSecondary)
		s.configure("TButton", background=self.options.colorPrimary, foreground=self.options.colorSecondary,pady=10)


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
			npmThread = GetNpmDataThread(packageName)
			addLoader(self.tabInfo,self.options)
			addLoader(self.tabReadMe,self.options)
			addLoader(self.tabDownload,self.options)
			npmThread.start()
			self.scheduleCheckThread(npmThread)

	def scheduleCheckThread(self,threadNpm:GetNpmDataThread):
		self.after(1000, self.checkDataReady, threadNpm)

	def checkDataReady(self, threadNpm:GetNpmDataThread):
		if not threadNpm.is_alive():
			if threadNpm.hasError:
				self.showPopupError(threadNpm.errMsg)
			else:
				self.updateGeneralInfoTab(threadNpm.dataToShow)
				self.updateDownloadInfoTab(threadNpm.dataToShow,threadNpm.nbTotalDownload,threadNpm.listDownloadsThirty)
		else:
			self.scheduleCheckThread(threadNpm)

	def updateGeneralInfoTab(self, dataFromNpm):
		for child in self.tabInfo.winfo_children():
			child.destroy()
		InfoPackageWidget(self.tabInfo, dataFromNpm,self.options).pack()
		for child in self.tabReadMe.winfo_children():
			child.destroy()
		ReadMeViewerWidget(self.tabReadMe, dataFromNpm,self.options).pack()

	def updateDownloadInfoTab(self, generalDataFromNpm, sumDownload,listDownloadsThirty):
		"""
		Show tab with package download informations
		"""
		for child in self.tabDownload.winfo_children():
			child.destroy()
		GraphDownloadsWidget(self.tabDownload, generalDataFromNpm, sumDownload,listDownloadsThirty,self.options).pack()	

	def showPopupError(self, message="Une erreur est survenue"):
		"""
		Show error popup
		"""
		ErrorPopup(self,self.options, message)


if __name__ == "__main__":
	options= getGUIOptions("config.properties","dev")
	app = MyApp(options)
	app.mainloop()
		


