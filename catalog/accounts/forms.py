from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .serializers import CaptchaFieldSerializer


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    captcha = CaptchaFieldSerializer()

    class Meta:
        model = User
        extra_fields = ["email"]
        fields = ["username", "password1", "password2"]


class ProfileUpdateForm(forms.Form):
    email = forms.EmailField(label="Email:")
    avatar = forms.ImageField(required=False, label="Avatar:")

    def clean_email(self):
        new_email = self.cleaned_data.get("email")
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("User with this Email Already Exists")
        else:
            return new_email

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["email"].initial = self.user.email


class RegisterFormNoCaptcha(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="Login:")
    password = forms.CharField(
        widget=forms.PasswordInput(), required=True, label="Password:"
    )
