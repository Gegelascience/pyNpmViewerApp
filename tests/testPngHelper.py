from modules.picture.controllers.PngGenerator import PngBuilder, PicturePixels, Pixel
import unittest
from tkinter import PhotoImage, Tk
import os


class PngHelperTestCase(unittest.TestCase):

    def setUp(self) -> None:
        actualData = PicturePixels()

        row =0
        while row < 32:
            col = 0
            rowData = []
            while col < 32:
                if row > 2 and row <29 and (col in [4,5,6,25,26,27] or col==row or col == row+1 or col == row-1):

                    rowData.append(Pixel(red=255,green=255,blue=255,alpha=255))
                else:
                    rowData.append(Pixel(red=255,green=0,blue=0,alpha=255))
                col+=1
            actualData.addRow(rowData)	
            row+=1

        self.photoBuilder = PngBuilder(actualData,32,32)

    def test_pngMagicNumberCompliant(self):
        
        data=self.photoBuilder.binaryContent
        self.assertEqual(data[0:8], b'\x89PNG\r\n\x1a\n')

    def test_structurePngOK(self):

        if os.environ.get('DISPLAY','') == '':
            print('no display found. Using :1.0')
            statusVirtualScreen = os.system('Xvfb :1 -screen 0 1600x1200x16  &')
            print("virtual screen command status",statusVirtualScreen)
            os.environ['DISPLAY'] = ':1.0'
        testApp = Tk()
        testApp.withdraw()
        PhotoImage(master=testApp,data= self.photoBuilder.binaryContent)