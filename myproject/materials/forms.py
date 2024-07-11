# materials/forms.py
from django import forms
from .models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'lectures', 'classes', 'labs', 'projects']
