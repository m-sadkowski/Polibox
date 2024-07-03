from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password2 = forms.CharField(
        label="Potwierdź hasło",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='',
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@student.pg.edu.pl"):
            raise forms.ValidationError("Email musi być z domeny @student.pg.edu.pl")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Istnieje zarejestrowany użytkownik z takim adresem email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"].split('@')[0]
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            username = username.split('@')[0]  # Pobierz nazwę użytkownika przed '@'
        return username
