import json
import pathlib
import gradio_client
from .models import Image
from django.db.models import Q
from .forms import ImageUploadForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
# Create your views here.

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


@login_required(login_url='/accounts/login')
def selectPlant(request):
    context = {}
    template_name = "predictor/select.html"
    return render(request=request, template_name=template_name, context=context)


def uploadImage(request, plant_name):
    if request.method == 'GET':
        form = ImageUploadForm()
        try:
            images = Image.objects.filter(
                Q(user=request.user) & Q(name=plant_name))
            context = {"form": form, "images": images,
                       "plant_name": plant_name}
            template_name = "predictor/predict.html"
        except Exception as e:
            context = {
                "error": e, 'message': 'An error occured while fetching your old images'}
            template_name = "plants/error.html"
            return render(request=request, template_name=template_name, context=context)
        return render(request=request, template_name=template_name, context=context)

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
        context = {"form": form, "images": images}
        template_name = "predictor/predict.html"
    return render(request=request, template_name=template_name, context=context)


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
        image_url = images[0].image.url
    except Image.DoesNotExist as e:
        context = {
            'error': e,
            'message': 'The selected image does not exist, try uploading another image.'
        }
        template_name = "plants/error.html"
        return render(request=request, template_name=template_name, context=context)

    except IndexError as e:
        context = {
            'error': e,
            'message': 'You have not uploaded any images yet.'
        }
        template_name = "plants/error.html"
        return render(request=request, template_name=template_name, context=context)

    # # Define the API endpoint
    try:
        api_endpoint = f"https://deepconclusions-{plant_name}.hf.space/"
        client = gradio_client.Client(api_endpoint)
        response = client.predict(
            # str (filepath or URL to image) in 'img' Image component
            f"{BASE_DIR}{image_url}",
            api_name="/predict"
        )

        with open(response, 'r') as file:
            result = json.load(file)

        context = {"image": images[0],
                   "result": result, "plant_name": plant_name}
        template_name = "predictor/result.html"
    except Exception as e:
        context = {
            'error': e,
            'message': 'You can not make predictions now'
        }
        template_name = "plants/error.html"
        return render(request=request, template_name=template_name, context=context)

    return render(request=request, template_name=template_name, context=context)
