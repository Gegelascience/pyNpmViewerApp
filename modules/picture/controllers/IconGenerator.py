from modules.picture.generator.PngGenerator import PngBuilder, PicturePixels, Pixel
import struct

def returnIconHeaderValue():
	return struct.pack('<hhh', 0, 1, 1)

def returnIconDirectory(width:int, height:int):
	widthConfig = width if width < 256 else 0
	heightConfig = height if height < 256 else 0
	directoryBytes = struct.pack("<BBBBhhII",widthConfig, heightConfig, 1,0,0,1,width*height*4,22)
	return directoryBytes

def createIcon(actualData:PicturePixels,width:int,height:int):
	
	header = returnIconHeaderValue()
	icondirectory = returnIconDirectory(width,height)
	pngElement = PngBuilder(actualData,width,height)

	return b"".join([header,icondirectory,pngElement.binaryContent])


if __name__ == "__main__":
	actualData = PicturePixels()
	row =0
	while row < 32:
		col = 0
		rowData = []
		while col < 32:
			rowData.append(Pixel(red=255,green=127,blue=0,alpha=255))
			col+=1
		actualData.addRow(rowData)	
		row+=1

	iconFilebinary =createIcon(actualData, 32,32)

	with open("test.ico","wb") as icoFile:
		icoFile.write(iconFilebinary)