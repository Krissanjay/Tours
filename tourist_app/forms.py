from django import forms

from .models import *


class TourForm(forms.ModelForm):
    image1=models.FileField()
    image2=models.FileField()

    class Meta:
        model=Tour
        fields='__all__'