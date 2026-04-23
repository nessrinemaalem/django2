from django import forms
from .models import People

class SearchForm(forms.Form):
    release_date_min = forms.DateField(label="Movies minimum release date")
    release_date_max = forms.DateField(label="Movies maximum release date")
    diameter_min = forms.IntegerField(label="Planet diameter greater than")
    gender = forms.ChoiceField(label="Gender")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genders = (
            People.objects
            .exclude(gender__isnull=True)
            .exclude(gender='')
            .values_list('gender', flat=True)
            .distinct()
            .order_by('gender')
        )
        self.fields['gender'].choices = [(g, g) for g in genders]
