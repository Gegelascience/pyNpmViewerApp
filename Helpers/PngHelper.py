import zlib
import struct


def createPng(rawData, height, width):
	
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
	IHDR[3] = struct.pack('>I', zlib.crc32(('IHDR' + IHDR[2].decode()).encode()))


	# IDAT
	IDAT = ['', '', '', '']
	IDAT[1] = u'IDAT'.encode('ascii')
	IDAT[2] = image_compressee
	IDAT[0] = struct.pack('>I', len(IDAT[2]))
	IDAT[3] = struct.pack('>I', zlib.crc32((str(IDAT[1]) + str(IDAT[2])).encode()))

	# IEND
	IEND = ['', '', '', '']
	IEND[1] = u'IEND'.encode('ascii')
	IEND[0] = struct.pack('>I', len(IEND[2]))
	IEND[3] = struct.pack('>I', zlib.crc32(('IEND' + IEND[2]).encode()))


	pngBytesContent = []

	pngBytesContent.extend(signature)
	pngBytesContent.extend(IHDR)
	pngBytesContent.extend(IDAT)
	pngBytesContent.extend(IEND)

	return pngBytesContent

if __name__ == "__main__":

	test= [
		[ (255, 0, 0,255),(0, 255, 0,255)],
		[ (0, 0, 255,255),(255, 255, 255,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
		[ (0, 0, 0,255),(0, 0, 0,255)],
	]
	pngContent = createPng(test,4,2)

	with open("test.png","wb") as pngTest:
		for el in pngContent:
			if isinstance(el,int):
				pngTest.write(el.to_bytes(1, byteorder='little'))
			elif isinstance(el,str):
				if len(el) > 0:
					pngTest.write(bytearray(el,encoding="utf-8"))
			else:
				pngTest.write(el)