from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@student.pg.edu.pl"):
            raise forms.ValidationError("Email musi być z domeny @student.pg.edu.pl")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"].split('@')[0]
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Nazwa użytkownika - s<nr_albumu> (np. s123456)")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            username = username.split('@')[0]  # Pobierz nazwę użytkownika przed '@'
        return username
