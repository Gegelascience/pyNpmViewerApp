import zlib
import struct

class PngBuilder:
	byteContentList:list = []

	def __init__(self,rawData,height:int, width:int) -> None:
		image = []

		for ligne in rawData:
			image.append(0)
			ligneInt = []
			for pixel in ligne:
				ligneInt.extend(pixel)
			image.extend(ligneInt)

		image_compressee = zlib.compress(bytearray(image))
		

		# magic number
		signature = struct.pack('>BBBBBBBB', 137, 80, 78, 71, 13, 10, 26,10)

		# IDHR
		IHDR = ['', '', '', ''] # Les 4 éléments d'un bloc
		IHDR[1] = u'IHDR'.encode('ascii')
		IHDR[2] = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
		IHDR[0] = struct.pack('>I', len(IHDR[2]))
		IHDR[3] = struct.pack('>I', zlib.crc32(IHDR[2], zlib.crc32(struct.pack('>4s', u'IHDR'.encode('ascii')))))


		# IDAT
		IDAT = ['', '', '', '']
		IDAT[1] = u'IDAT'.encode('ascii')
		IDAT[2] = image_compressee
		IDAT[0] = struct.pack('>I', len(IDAT[2]))
		IDAT[3] = struct.pack('>I', zlib.crc32(IDAT[2], zlib.crc32(struct.pack('>4s', u'IDAT'.encode('ascii')))))

		# IEND
		IEND = ['', '', '', '']
		IEND[1] = u'IEND'.encode('ascii')
		IEND[0] = struct.pack('>I', len(IEND[2]))
		IEND[3] = struct.pack('>I', zlib.crc32(IEND[2].encode(), zlib.crc32(struct.pack('>4s', u'IEND'.encode('ascii')))))


		pngBytesNearlyOK = []

		pngBytesNearlyOK.extend(signature)
		pngBytesNearlyOK.extend(IHDR)
		pngBytesNearlyOK.extend(IDAT)
		pngBytesNearlyOK.extend(IEND)

		for el in pngBytesNearlyOK:
			if isinstance(el,int):
				self.byteContentList.append(el.to_bytes(1, byteorder='little'))
			elif isinstance(el,str):
				if len(el) > 0:
					self.byteContentList.append(bytearray(el,encoding="utf-8"))
			else:
				self.byteContentList.append(el)


	def writeFile(self,filePath:str):
		with open(filePath,"wb") as pngFile:
			for el in self.byteContentList:
				pngFile.write(el)

if __name__ == "__main__":

	test= [
		[ (255, 0, 0,255),(0, 255, 0,255)],
		[ (0, 0, 255,255),(255, 255, 255,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
	]
	pngBuilder = PngBuilder(test,4,2)
	pngBuilder.writeFile("test.png")
