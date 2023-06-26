import json
import pathlib
import requests
import gradio_client
from .models import Image
from django.db.models import Q
from .forms import ImageUploadForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
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
    return redirect("predictor:upload_image", plant_name)


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
    api_endpoint = f"https://deepconclusions-{plant_name}.hf.space/"
    client = gradio_client.Client(api_endpoint)
    response = client.predict(
        # str (filepath or URL to image) in 'img' Image component
        f"{BASE_DIR}{image_url}",
        api_name="/predict"
    )

    with open(response, 'r') as file:
        result = json.load(file)

    print(result)

    return render(request, "predictor/result.html", {"image": images[0], "result": result, "plant_name": plant_name})
