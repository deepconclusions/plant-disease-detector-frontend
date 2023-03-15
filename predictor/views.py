import requests
import pathlib
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


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
    return redirect("predictor:upload_image/", plant_name)


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
    # # Define the API endpoint
    # api_endpoint = 'http://127.0.0.1:8000/corn/single-prediction/'

    # # Set the headers
    # headers = {'Content-Type': 'multipart/form-data'}

    # # Create a dictionary with the image file and any other form data you want to send
    # data = {'image': open(f"{BASE_DIR}{image_url}", 'rb')}

    # print(data)
    # # Send the POST request
    # response = requests.post(api_endpoint, headers=headers, files=data)

    # # If the request was successful, parse the JSON response
    # if response.status_code == 200:
    #     json_response = response.json()
    #     # Do something with the JSON response
    #     print(json_response)
    #     return json_response
    # else:
    #     # Handle the error
    #     print(f'Request failed with status code {response.status_code}')
    result = {
        "prediction": 999,
        "label": "No predicton",
        "confidence": 0.0,
        "description": "No description",
        "value_error": f"Either No {plant_name} image is provided or It is not labelled, make sure to label with 'corn-image'"
    }

    return render(request, "predictor/result.html", {"image": images[0], "result": result, "plant_name":plant_name})
