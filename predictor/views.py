import requests
import pathlib
from django.shortcuts import render, redirect, HttpResponse
from .forms import ImageUploadForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


@login_required(login_url='/accounts/login')
def selectPlant(request):
    return render(request, "predictor/select.html", {})


def uploadImage(request, plant_name):
    if request.method == 'GET':
        form = ImageUploadForm()
        try:
            images = Image.objects.filter(
                Q(user=request.user) & Q(name=plant_name))
            print(f"images:{images}")
        except Exception as e:
            print(e)  # Debug output
            images = []
        return render(request, "predictor/predict.html", {"form": form, "images": images, "plant_name": plant_name})

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image()
            image.image = form.cleaned_data['image']
            image.name = plant_name
            image.user = request.user
            image.save()
            return redirect('predictor:upload_image', plant_name)
    else:
        form = ImageUploadForm()
        images = Image.objects.filter(
            Q(user=request.user) & Q(name=plant_name))
    return render(request, "predictor/predict.html", {"form": form, "images": images})


def deleteImage(request, plant_name, id):
    image = get_object_or_404(Image, id=id)
    image.delete()
    return redirect("predictor:upload_image", plant_name )


def getPredictions(request, plant_name):
    # get image path
    try:
        images = Image.objects.filter(
            Q(user=request.user) & Q(name=plant_name))
        print(f"images:{images}")
    except Exception as e:
        print(e)  # Debug output
        images = []
    image_url = images[0].image.url
    # Define the API endpoint
    api_endpoint = f'http://127.0.0.1:8001/{plant_name}/single-prediction/'

    # Set the headers
    headers = {}

    # Set payload
    payload = {}

    # Create a dictionary with the image file and any other form data you want to send
    files = [(f'{plant_name}-image', open(f"{BASE_DIR}{pathlib.Path(image_url)}", 'rb'))]

    print(colored(0, 0, 255, f"{BASE_DIR}{pathlib.Path(image_url)}"))

    # Send the POST request
    response = requests.post(api_endpoint, headers=headers, files=files)
    # response = requests.get(api_endpoint)
    print(colored(0, 0, 255, str(response)))

    # If the request was successful, parse the JSON response
    if response.status_code == 200:
        json_response = response.json()
        # Do something with the JSON response
        return render(request, "predictor/result.html", {"image": images[0], "result": json_response, "plant_name":plant_name})
    else:
        # Handle the error
        return HttpResponse(f'Request failed with status code {response.status_code}')
