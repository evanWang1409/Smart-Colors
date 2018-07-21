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

def getDataFromCloth(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for cloth in root: 
        ccolor = []
        for attri in cloth:
            if attri.tag == "type":
                name = attri.text
            elif attri.tag == "gender":
                gender = attri.text[0].upper()
            elif attri.tag == "name":
                name += "-" + attri.text
            elif attri.tag == "url":
                url = attri.text
            else:
                # attri.tag = color
                for hexValue in attri:

                    print(hexValue.text)
                    ccolor.append(hexValue.text)
        colorObj = color(combination=json.dumps(ccolor))
        colorObj.save()
        elem = pic(name=name, url=url, gender=gender, colors=colorObj)
        elem.save()

from findColor.models import color, pic, userPhoto
#getDataFromColor("findColor/result3_(150-250).xml")
getDataFromCloth("findColor/cloth.xml")