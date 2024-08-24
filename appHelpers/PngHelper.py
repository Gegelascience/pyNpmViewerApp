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

	def __init__(self,rawData: list,height:int, width:int, colorMode:PngColorType=PngColorType.RGBA) -> None:
		
		pngBytesNearlyOK = []

		# magic number
		pngBytesNearlyOK.append(struct.pack('>BBBBBBBB', 137, 80, 78, 71, 13, 10, 26,10))

		print(colorMode.value)
		
		# IDHR
		pngBytesNearlyOK.append(PngChunkBuilder(PngChunkName.IHDR,struct.pack('>IIBBBBB', width, height, 8, colorMode.value, 0, 0, 0)).getBytesContent())

		# IDAT
		image = []

		for ligne in rawData:
			image.append(0)
			ligneInt = []
			for pixel in ligne:
				ligneInt.extend(pixel)
			image.extend(ligneInt)

		image_compressee = zlib.compress(bytearray(image))

		pngBytesNearlyOK.append(PngChunkBuilder(PngChunkName.IDAT,image_compressee).getBytesContent())

		# IEND
		pngBytesNearlyOK.append(PngChunkBuilder(PngChunkName.IEND,b"").getBytesContent())

		self.binaryContent = b"".join(pngBytesNearlyOK)


	def writeFile(self,filePath:str):
		with open(filePath,"wb") as pngFile:
			pngFile.write(self.binaryContent)

if __name__ == "__main__":

	test= [
		[ (255, 0, 0,255),(0, 255, 0,255)],
		[ (0, 0, 255,255),(255, 255, 255,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
	]
	pngBuilder = PngBuilder(test,4,2)
	pngBuilder.writeFile("test.png")
