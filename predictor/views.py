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
from django.shortcuts import render, redirect
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


def getGeneralPredictions(filename):
    API_URL = "https://api-inference.huggingface.co/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
    headers = {"Authorization": "Bearer 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"}

    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)

    return response.json()


def getDescription(result):
    API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": f"What causes {result['label']} and how can it be controlled",
    })

    print(f"output: {output}")
    return output[0]["generated_text"]


def getSpecificPrediction(filename, plant_name):
    api_endpoint = f"https://deepconclusions-{plant_name}.hf.space/"
    client = gradio_client.Client(api_endpoint)
    response = client.predict(
        # str (filepath or URL to image) in 'img' Image component
        filename,
        api_name="/predict"
    )

    with open(response, 'r') as file:
        result = json.load(file)

    return result['label']


def getPredictions(request, plant_name):
    context = {"plant_name": plant_name}

    # get image path
    try:
        images = Image.objects.filter(
            Q(user=request.user) & Q(name=plant_name))
        print(f"images:{images}")
        image_url = images[0].image.url
        context['image'] = images[0]
    except Image.DoesNotExist as e:
        context['error'] = e,
        context['message'] = 'The selected image does not exist, try uploading another image.'
        template_name = "plants/error.html"
        return render(request=request, template_name=template_name, context=context)

    except IndexError as e:
        context['error'] = e,
        context['message'] = 'You have not uploaded any images yet.'
        template_name = "plants/error.html"
        return render(request=request, template_name=template_name, context=context)

    # # Define the API endpoint
    try:
        if plant_name == 'general':
            result = getGeneralPredictions(f"{BASE_DIR}{image_url}")[0]
            # description = getDescription(result)
            context['description'] = ''
            context['result'] = result['label']
            print(f"result: {result}")
        else:
            result = getSpecificPrediction(f"{BASE_DIR}{image_url}", plant_name)
            # description = getDescription(result)
            context['description'] = ''
            context['result'] = result
            print(f"result: {result}")
            
    except Exception as e:
        context['error'] = e,
        context['message'] = 'You can not make predictions now'
        template_name = "plants/error.html"
        return render(request=request, template_name=template_name, context=context)
    
    template_name = "predictor/result.html"
    return render(request=request, template_name=template_name, context=context)
