from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'plants/home.html')


def about(request):
    return render(request, 'plants/about.html')

def pricing(request):
    return render(request, 'plants/pricing.html')

def support(request):
    return render(request, "plants/support.html")

def careers(request):
    return render(request, "plants/careers.html")

def videos(request):
    return render(request, "plants/videos.html")
