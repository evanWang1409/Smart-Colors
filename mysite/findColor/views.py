from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(
        request,
        'index.html',
        # context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},
    )
    # return HttpResponse("Get color combination...")