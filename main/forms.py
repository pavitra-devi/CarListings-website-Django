from django import forms

from .models import Listing

class ListingForm(forms.ModelForm):
    #image = forms.ImageField(required=False)
    image = forms.ImageField()
    class Meta:
        model= Listing
        fields = {'brand','model','mileage','color','description','engine','transmission','image'}


