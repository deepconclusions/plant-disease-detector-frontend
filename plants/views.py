from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'plants/home.html')


def about(request):
    return render(request, 'plants/about.html')
