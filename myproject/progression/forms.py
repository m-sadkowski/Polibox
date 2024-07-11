from django import forms
from .models import UserProgress


class UserProgressForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ['element', 'completed']
