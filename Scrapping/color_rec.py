#copyright@why
#whynull@sjtu.edu.cn

from bs4 import BeautifulSoup
import webcolors
#import urllib.request
import re, cv2
import os
#import urllib
import sys
import time
import requests
import scrapping_color_rec
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET

img_temp_path = '/Users/evnw/Programming/Colors/Smart-Colors/Scrapping/test.jpg'
xml_path = '/Users/evnw/Programming/Colors/Smart-Colors/Scrapping/cloth.xml'

class feature:
    def __init__(self,gender,type,name, hex_code, url):
        self.gender = gender
        self.type = type
        self.name = name
        self.hex_code = hex_code
        self.url = url

def save(path_img,img):
    temp = ""
    colors = []
    while temp == "":
        try:
            response = requests.get(img)
            image = response.content
            f = open(img_temp_path,'wb')
            f.write(image)
            f.close()
            im = cv2.imread(img_temp_path)
            dom_colors = scrapping_color_rec.color_recognition(im)
            for color in dom_colors:
                colors.append(webcolors.rgb_to_hex((color[2], color[1], color[0])))
            temp = "OK"
        except:
            print("Sleeping")
            time.sleep(5)

    return colors


def read(str):
    strlist = str.split('/')
    return strlist[0],strlist[1],strlist[2]

def operate(path_data,path_img):
    root = ET.Element("Outfit")
    f = open(path_data,"r")
    stat = 0
    gender = None
    cloth_type = None
    name = None

    for line in f:
        if stat == 0:
            gender, cloth_type, name = read(str(line)[str(line).find("product")+8:str(line).find("#")])

        if stat == 1:
            url = str(line)
            colors = save(path_img,url)
            data = feature(gender, cloth_type, name, colors, url)
            cloth = ET.SubElement(root, "cloth")
            ET.SubElement(cloth, "gender").text = "{}".format(gender)
            ET.SubElement(cloth, "type").text = "{}".format(cloth_type)
            ET.SubElement(cloth, "name").text = "{}".format(name)
            ET.SubElement(cloth, "url").text = "{}".format(url)
            color_node = ET.SubElement(cloth, 'color')
            for hex_color in colors:
                print (hex_color)
                ET.SubElement(color_node, "hex").text = "{}".format(hex_color)
            gender = None
            cloth_type = None
            name = None

        stat = 1 - stat
        
    tree = ET.ElementTree(root)
    tree.write(xml_path)

    f.close()


def main():
    path_data = "/Users/evnw/Programming/Colors/scrap_img/data.txt"
    path_image = "/Users/evnw/Programming/Colors/scrap_img"
    operate(path_data,path_image)

main()
