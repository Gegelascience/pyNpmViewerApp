import zlib
import struct
from enum import Enum, unique

@unique
class PngChunkName(Enum):
	IHDR="IHDR"
	IDAT="IDAT"
	IEND="IEND"
	PLTE="PLTE"

@unique
class PngColorType(Enum):
	RGB=2
	RGBA=6
	GRAY=0
	GRAYSCALEALPHA=4

class Pixel:

	def __init__(self,red:int=0,green:int=0,blue:int=0,alpha:int=0,gray:int=0):
		if not self.__checkCorrectValue(red):
			raise Exception("invalid red value")
		self.__red = red
		if not self.__checkCorrectValue(green):
			raise Exception("invalid green value")
		self.__green = green
		if not self.__checkCorrectValue(blue):
			raise Exception("invalid blue value")
		self.__blue = blue
		if not self.__checkCorrectValue(gray):
			raise Exception("invalid gray value")
		self.__gray = gray

		if not self.__checkCorrectValue(alpha):
			raise Exception("invalid alpha value")
		self.__alpha = alpha

	def setRed(self,val:int):
		if self.__checkCorrectValue(val):
			self.__red = val

	def setGreen(self, val:int):
		if self.__checkCorrectValue(val):
			self.__green = val

	def setBlue(self, val:int):
		if self.__checkCorrectValue(val):
			self.__blue = val

	def setGray(self, val:int):
		if self.__checkCorrectValue(val):
			self.__gray = val

	def setAlpha(self, val:int):
		if self.__checkCorrectValue(val):
			self.__alpha = val

	def __checkCorrectValue(self,val:int):
		return val >=0 and val <=255

	def getPixelData(self,colorMode: PngColorType):
		if colorMode == PngColorType.RGB:
			return (self.__red, self.__green,self.__blue)
		elif colorMode == PngColorType.RGBA:
			return (self.__red, self.__green,self.__blue, self.__alpha)
		elif colorMode == PngColorType.GRAY:
			return (self.__gray)
		elif colorMode == PngColorType.GRAYSCALEALPHA:
			return (self.__gray, self.__alpha)
		
class PicturePixels:

	def __init__(self):
		self.__pixelRows:list[list[Pixel]] = []
		self.__lenRow = 0

	def addRow(self,rowPixel:list[Pixel]):
		if self.__lenRow > 0 and len(rowPixel) != self.__lenRow:
			raise Exception("Invalid row, wrong number of pixels")
		if self.__lenRow == 0:
			self.__lenRow = len(rowPixel)
		self.__pixelRows.append(rowPixel)

	def clearPixels(self):
		self.__pixelRows = []

	def getListRowPixels(self):
		return self.__pixelRows

	def getPixelsForPngBuilder(self, colorMode: PngColorType):
		listPixels = []
		for row in self.__pixelRows:
			rowPlain = []
			for pixel in row:
				rowPlain.extend(pixel.getPixelData(colorMode))

			listPixels.append(rowPlain)
		
		return listPixels

class PngChunkBuilder:

	def __init__(self,chunkName:PngChunkName,data:bytes):
		self.__chunkType = chunkName.value.encode("ascii")
		if chunkName != PngChunkName.IEND:
			self.__chunkData = data
			self.__chunkDataLen = struct.pack('>I', len(data))
			if chunkName ==PngChunkName.PLTE and len(data)%3 !=0:
				raise Exception("invalid palette data")
		else:
			self.__chunkData= "".encode()
			self.__chunkDataLen =struct.pack('>I', 0)
		self.__chunkCRC = struct.pack('>I', zlib.crc32(self.__chunkData, zlib.crc32(struct.pack('>4s', self.__chunkType))))

	def getBytesContent(self):
		return b"".join([self.__chunkDataLen,self.__chunkType, self.__chunkData, self.__chunkCRC])

class PngBuilder:
	binaryContent:bytes

	def __init__(self,rawData: PicturePixels,height:int, width:int, colorMode:PngColorType=PngColorType.RGBA) -> None:
		
		pngBytesNearlyOK = []

		# magic number
		pngBytesNearlyOK.append(struct.pack('>BBBBBBBB', 137, 80, 78, 71, 13, 10, 26,10))

		
		# IDHR
		pngBytesNearlyOK.append(PngChunkBuilder(PngChunkName.IHDR,struct.pack('>IIBBBBB', width, height, 8, colorMode.value, 0, 0, 0)).getBytesContent())

		# IDAT
		image = []

		rows = rawData.getPixelsForPngBuilder(colorMode)
		for row in rows:
			image.append(0)
			image.extend(row)

		image_compressee = zlib.compress(bytearray(image))

		pngBytesNearlyOK.append(PngChunkBuilder(PngChunkName.IDAT,image_compressee).getBytesContent())

		# IEND
		pngBytesNearlyOK.append(PngChunkBuilder(PngChunkName.IEND,b"").getBytesContent())

		self.binaryContent = b"".join(pngBytesNearlyOK)


	def writeFile(self,filePath:str):
		with open(filePath,"wb") as pngFile:
			pngFile.write(self.binaryContent)

if __name__ == "__main__":

	"""test= [
		[ (255, 0, 0,255),(0, 255, 0,255)],
		[ (0, 0, 255,255),(255, 255, 255,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
	]"""

	test = PicturePixels()

	test.addRow([Pixel(red=255,green=0,blue=0,alpha=255),Pixel(red=0,green=255,blue=0,alpha=255)])
	test.addRow([Pixel(red=0,green=0,blue=255,alpha=255),Pixel(red=255,green=255,blue=255,alpha=255)])
	test.addRow([Pixel(red=0,green=0,blue=0,alpha=255),Pixel(red=0,green=0,blue=0,alpha=255)])
	test.addRow([Pixel(red=0,green=0,blue=0,alpha=255),Pixel(red=0,green=0,blue=0,alpha=255)])
	
	pngBuilder = PngBuilder(test,4,2)
	pngBuilder.writeFile("test.png")
