from PngHelper import PngBuilder


def returnIconHeaderValue():
	# ico with 1 image
	return [0,0,1,0,1,0]

def returnIconDirectory(width, height):
	#ico 16x16
	directoryData = []
	# largeur
	directoryData.append(width)
	# hauteur
	directoryData.append(height)
	
	# 1 couleur
	directoryData.append(1)
	# 0 reserve
	directoryData.append(0)
	
	# color plane
	directoryData.append(0)
	directoryData.append(0)
	
	# bit par pixel
	directoryData.append(1)
	directoryData.append(0)

	# data size in bytes
	directoryData.append(0)
	directoryData.append(4)
	directoryData.append(0)
	directoryData.append(0)

	# offset data
	directoryData.append(22)
	directoryData.append(0)
	directoryData.append(0)
	directoryData.append(0)


	return directoryData

def createIcon(actualData,width,height):
	icoFileHeaders = []
	
	header = returnIconHeaderValue()
	directory = returnIconDirectory(width,height)

	pngElement = PngBuilder(actualData,width,height)

	icoFileHeaders.extend(header)
	icoFileHeaders.extend(directory)

	icoBytes = []
	for byte in icoFileHeaders:
		#print("byte",byte )
		icoBytes.append(byte.to_bytes(1, byteorder='little'))

	for el in pngElement.byteContentList:
		icoBytes.append(el)

	return icoBytes

	




if __name__ == "__main__":
	actualData = []
	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			rowData.append([255,255,255,255])
			col+=1
		actualData.append(rowData)	
		row+=1

	iconFileContent =createIcon(actualData, 32,32)

	with open("test.ico","wb") as icoFile:

		for el in iconFileContent:
			icoFile.write(el)