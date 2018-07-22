from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import color, pic, userPhoto
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from io import StringIO
import json
from rest_framework.decorators import api_view
import webcolors
import numpy as np
from Color_Identification import crop_color_rec
import sys
sys.path.insert(0,'/Users/evnw/Programming/Colors/Smart-Colors/darknetpy') 
import recognition
import cv2, os, time
import re

shuiguole = False
# Create your views here.

#targetColor = "#000000"

def getFrom(targetColor, allColors):
    jsonDec = json.decoder.JSONDecoder()
    result = []
    target_RGB = webcolors.hex_to_rgb(targetColor)
    min_dist = 9999999
    closest_colorStr = None
    for colorStr in allColors:
        colorList = jsonDec.decode(colorStr.combination)
        if targetColor in colorList:
            result.append(colorStr)
        local_min_dist = 9999999
        local_closest_color = None
        for color_hex in colorList:
            color_rgb = webcolors.hex_to_rgb(color_hex)
            color1 = color_rgb
            color2 = target_RGB
            dist = np.sqrt((int(color1[0]) - int(color2[0]))**2 + (int(color1[1]) - int(color2[1]))**2 + (int(color1[2]) - int(color2[2]))**2)
            if dist < local_min_dist:
                local_min_dist = dist
                local_closest_color = color_hex

        if local_min_dist < min_dist:
            min_dist = local_min_dist
            closest_color = local_closest_color
            closest_colorStr = colorStr

    if len(result) == 0:
        return [closest_colorStr]

    return result

def getClothesFrom(targetColor, allClothes):
    jsonDec = json.decoder.JSONDecoder()
    result = []
    target_RGB = webcolors.hex_to_rgb(targetColor)
    min_dist = 9999999
    closest_color = None
    closest_obj = None
    for clothObj in allClothes:
        colorList = jsonDec.decode(clothObj.colors.combination)
        if targetColor in colorList:
            result.append(clothObj)
        local_min_dist = 9999999
        local_closest_color = None
        for color_hex in colorList:
            color_rgb = webcolors.hex_to_rgb(color_hex)
            color1 = color_rgb
            color2 = target_RGB
            dist = np.sqrt((int(color1[0]) - int(color2[0]))**2 + (int(color1[1]) - int(color2[1]))**2 + (int(color1[2]) - int(color2[2]))**2)
            if dist < local_min_dist:
                local_min_dist = dist
                local_closest_color = color_hex
        if local_min_dist < min_dist:
            min_dist = local_min_dist
            closest_color = local_closest_color
            closest_obj = clothObj
        #print(closest_obj)

    backup_result = [closest_obj]

    if len(result) == 0:
        return backup_result

    return result

#def color_dist(color1, color2):
#    return np.sqrt((int(color1[0]) - int(color2[0]))**2 + (int(color1[1]) - int(color2[1]))**2 + (int(color1[2]) - int(color2[2]))**2)

@api_view(['GET', 'POST'])
def getColorData(request):
    jsonDec = json.decoder.JSONDecoder()
    if request.method == "POST":
        color = request.POST.get('data')
        print(color)
        return color

@csrf_exempt
def index(request):

    global shuiguole

    img_path = '/Users/evnw/Downloads/image.png'
    jud = True
    while jud or not request.method == "POST":
        try:
            im_temp = cv2.imread(img_path)[::-1]
            jud = False
        except:
            time.sleep(1)
    #im = Image.open(StringIO(request.FILES['im']['content']))
    #im.save("D:/code", "PNG")

    #getColors = '#ffffff'
    #getClothes = None
    #detector = recognition.initialize()
    #im_crop = recognition.yolo_detect(img_path, detector)
    im_crop = cv2.imread(img_path)
    colors_BGR = crop_color_rec.color_detection(im_crop)
    colors_hex = []
    for BGR in colors_BGR:
        colors_hex.append(webcolors.rgb_to_hex((BGR[2], BGR[1], BGR[0])))
    jsonDec = json.decoder.JSONDecoder()
    allColors = color.objects.all()
    getColors = getFrom(colors_hex[0], allColors)
    print(getColors)
    print(len(getColors[0].getColors()))
    allClothes = pic.objects.all()
    getClothes = []
    for colorObj in getColors:
        # for colorObj in colorObjList:
        ccolor = jsonDec.decode(colorObj.combination)
        for colorOb in ccolor:
            getClothes += getClothesFrom(colorOb, allClothes)


    
    if request.method == "POST" or shuiguole:
        print('postttttttttttttttttt')
        shuiguole = True
        
        getClothes = list(set(getClothes))
        print(getClothes)
        #selectedColor = getColorData(request)
        os.remove(img_path)
        return render(
        request,
        'index.html',
        context={'color_all': getColors, 'clothes' : getClothes}
        )
    else:
        print('eeeeelllllllllllllllllll')
        return render(
        request,
        'index.html',
        context={'color_all': getColors, 'clothes': getClothes}
        )
        
    # return HttpResponse("Get color combination...")