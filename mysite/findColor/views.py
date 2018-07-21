from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import color, pic, userPhoto
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from io import StringIO
# Create your views here.

def index(request):
    #im = Image.open(StringIO(request.FILES['im']['content']))
    #im.save("D:/code", "PNG")
    t = color.objects.all()[1]
    return render(
        request,
        'index.html',
        context={'color': t}
    )
    # return HttpResponse("Get color combination...")