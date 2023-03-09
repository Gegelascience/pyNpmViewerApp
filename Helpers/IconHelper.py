import PngHelper


def returnIconHeaderValue():
	# ico with 1 image
	return [0,0,1,0,1,0]

def returnIconDirectory():
	#ico 16x16
	directoryData = []
	# largeur
	directoryData.append(32)
	# longueur
	directoryData.append(32)
	
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

def createIcon():
	icoFileHeaders = []
	
	header = returnIconHeaderValue()
	directory = returnIconDirectory()

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

	dataPng = PngHelper.createPng(actualData,32,32)

	icoFileHeaders.extend(header)
	icoFileHeaders.extend(directory)



	with open("test.ico","wb") as icoFile:
		for byte in icoFileHeaders:
			#print("byte",byte )
			icoFile.write(byte.to_bytes(1, byteorder='little'))

		for el in dataPng:
			icoFile.write(el)




if __name__ == "__main__":
	createIcon()