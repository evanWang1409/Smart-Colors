import xml.etree.ElementTree as ET
import json

def getDataFromColor(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for child in root:
        L = []
        for colorStr in child:
            L.append(colorStr.text)
        elem = color(combination=json.dumps(L))
        elem.save()

from findColor.models import color, pic, userPhoto
getDataFromColor("findColor/result3_(150-250).xml")