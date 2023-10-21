from xml.etree import ElementTree as ET
from tkinter import Frame, Canvas,ttk, X

class LineChartWrapper:

    def __init__(self, datalist:list):
        self.data = datalist


    def drawCanvas(self,title:str, master:Frame, interValueSpace:int,primaryColor:str, secondaryColor:str,padding:tuple=(0,0)):
        maxValue = max(self.data)
        minValue = min(self.data)

        ttk.Label(master,text=title).pack()
        graph = Canvas(master,height=120,width=425, background=secondaryColor)
        graph.pack(fill=X,pady=padding)
            
        for i,dayStat in enumerate(self.data):
            if dayStat in (minValue,maxValue):
                graph.create_text(i*interValueSpace + 5,10,text=dayStat)
            if i > 0:
                graph.create_line((i-1)*interValueSpace + 5, 20+(maxValue-self.data[i-1])*100/maxValue, i*interValueSpace + 5, 20+(maxValue-dayStat)*100/maxValue,width=3, fill=primaryColor)

    def saveAsSvg(self, filepath):
        maxValue = max(self.data)
        minValue = min(self.data)
        
        initialStr = '''
            <svg version='1.1' baseProfile='full' width='700' height='200' xmlns='http://www.w3.org/2000/svg'>
            </svg>'''
        
        root = ET.XML(initialStr)
        graphZone = ET.SubElement(root,"g")

        for i,dayStat in enumerate(self.data):
            if dayStat in (minValue,maxValue):
                textTag = ET.SubElement(graphZone,"text")
                textTag.set("x",str(i*14 + 5))
                textTag.set("y",str(15))
                textTag.text = str(dayStat)
                textTag.set("color","black")

            if i > 0:

                line = ET.SubElement(graphZone,"line")
                line.set("stroke-width",str(3))
                line.set("y1",str(20+(maxValue-self.data[i-1])*100/maxValue))
                line.set("x1",str((i-1)*14 + 5))
                line.set("y2",str(20+(maxValue-dayStat)*100/maxValue))
                line.set("x2",str(i*14 + 5))
                line.set("stroke","red")

        tree = ET.ElementTree(root)
        ET.register_namespace("","http://www.w3.org/2000/svg")

        tree.write(filepath, encoding="utf-8",xml_declaration=True)