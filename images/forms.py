from django import forms
from datetime import timedelta

intervals = (
    (timedelta(days=100*365).total_seconds(), 'never'),
    (timedelta(minutes=1).total_seconds(), '1 minute'),
    (timedelta(minutes=10).total_seconds(), '10 minutes'),
    (timedelta(minutes=10).total_seconds(), '30 minutes'),
    (timedelta(hours=1).total_seconds(), '1 hour'),
    (timedelta(hours=1).total_seconds(), '12 hour'),
    (timedelta(days=1).total_seconds(), '1 day'),
    (timedelta(days=2).total_seconds(), '2 days'),
    (timedelta(days=7).total_seconds(), '7 days'),
    (timedelta(days=31).total_seconds(), '1 month'),
    (timedelta(days=6*31).total_seconds(), '6 months'),
    (timedelta(days=365).total_seconds(), '1 year'),
    (timedelta(days=2*365).total_seconds(), '2 years'),)


class UploadFileForm(forms.Form):
    your_name = forms.CharField(max_length=35, required=False)
    file = forms.ImageField()
    expiration = forms.ChoiceField(choices=intervals)
    # tagList = forms.ChoiceField(required=False)

class ClassifyFileForm(forms.Form):
    file = forms.ImageField()


