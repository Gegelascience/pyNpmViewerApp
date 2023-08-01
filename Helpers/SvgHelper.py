from xml.etree import ElementTree as ET

from models.NpmModels import PackageDownloadInfo

def saveGraphAsSvg(data:PackageDownloadInfo,filepath:str):

    maxValue = max(data.downloads)
    minValue = min(data.downloads)
    
    initialStr = '''
        <svg version='1.1' baseProfile='full' width='700' height='200' xmlns='http://www.w3.org/2000/svg'>
        </svg>'''
    
    root = ET.XML(initialStr)
    graphZone = ET.SubElement(root,"g")

    for i,dayStat in enumerate(data.downloads):
        if dayStat in (minValue,maxValue):
            textTag = ET.SubElement(graphZone,"text")
            textTag.set("x",str(i*14 + 5))
            textTag.set("y",str(15))
            textTag.text = str(dayStat)
            textTag.set("color","black")

        if i > 0:

            line = ET.SubElement(graphZone,"line")
            line.set("stroke-width",str(3))
            line.set("y1",str(20+(maxValue-data.downloads[i-1])*100/maxValue))
            line.set("x1",str((i-1)*14 + 5))
            line.set("y2",str(20+(maxValue-dayStat)*100/maxValue))
            line.set("x2",str(i*14 + 5))
            line.set("stroke","red")

    tree = ET.ElementTree(root)
    ET.register_namespace("","http://www.w3.org/2000/svg")

    tree.write(filepath, encoding="utf-8",xml_declaration=True)
