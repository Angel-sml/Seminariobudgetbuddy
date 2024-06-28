from django.forms import ModelForm
from .models import task
from django import forms
class taskform(ModelForm):
    class Meta:
        model = task
        fields = ['title', 'description', 'important']
        
class ValueForm(forms.Form):
    value = forms.FloatField(label='Valor Y', min_value=0)