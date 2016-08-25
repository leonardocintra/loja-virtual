from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    texts = ["maria puera", "Neymar fez gol na copa"]
    context = {
        "title": "django | e-commerce",
        "texts": texts
    }

    return render(request, 'index.html', context)