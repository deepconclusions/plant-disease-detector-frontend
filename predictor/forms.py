from django import forms


class ImageUploadForm(forms.Form):
    image = forms.FileField(
        label='Select an image',
        help_text='max. 2 megabytes'
    )
