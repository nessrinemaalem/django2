from django import forms

class TextForm(forms.Form):
    text = forms.CharField(
        label="Entrez du texte",
        max_length=100
    )
