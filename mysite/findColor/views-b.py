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

# Create your views here.

targetColor = "#000000"

def getFrom(targetColor, allColors):
    jsonDec = json.decoder.JSONDecoder()
    result = []
    for colorStr in allColors:
        colorList = jsonDec.decode(colorStr.combination)
        if targetColor in colorList:
            result.append(colorStr)
    return result

def getClothesFrom(targetColor, allClothes):
    jsonDec = json.decoder.JSONDecoder()
    result = []
    target_RGB = webcolors.hex_to_rgb(targetColor)
    min_dist = 9999999
    closest_color = None
    for clothObj in allClothes:
        colorList = jsonDec.decode(clothObj.colors.combination)
        if targetColor in colorList:
            result.append(clothObj)
        local_min_dist = 9999999
        local_closest_color = None
        for color_hex in colorList:
            color_rgb = webcolors.hex_to_rgb(color_hex)
            dist = color_dist(target_RGB, color_rgb)
            if dist < local_min_dist:
                local_min_dist = dist
                local_closest_color = color_hex
        if local_min_dist < min_dist:
            min_dist = local_min_dist
            closest_color = local_closest_color

    backup_result = [closest_color]

    if len(result) == 0:
        return backup_result

    return result

def color_dist(color1, color2):
    return np.sqrt((int(color1[0]) - int(color2[0]))**2 + (int(color1[1]) - int(color2[1]))**2 + (int(color1[2]) - int(color2[2]))**2)

@api_view(['GET', 'POST'])
def getColorData(request):
    jsonDec = json.decoder.JSONDecoder()
    if request.method == "POST":
        color = request.POST.get('data')
        print(color)
        return color

@csrf_exempt
def index(request):
    #im = Image.open(StringIO(request.FILES['im']['content']))
    #im.save("D:/code", "PNG")
    jsonDec = json.decoder.JSONDecoder()
    allColors = color.objects.all()
    getColors = getFrom(targetColor, allColors)
    allClothes = pic.objects.all()
    #for ccolor in getColors:
    ccolor = jsonDec.decode(getColors[0].combination)
    getClothes = getClothesFrom(ccolor, allClothes)
    if request.method == "POST":
        selectedColor = getColorData(request)
        print(selectedColor)
        return render(
        request,
        'index.html',
        context={'color': getColors}
        )
    else:
        return render(
        request,
        'index.html',
        context={'color': getColors, 'clothes': getClothes}
        )
    # return HttpResponse("Get color combination...")