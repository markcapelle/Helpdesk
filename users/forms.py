from django import forms
from django.contrib.auth.models import User, Group
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "avatar", "role"]

class UserSelfServiceForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]

class AdminUserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "avatar", "role"]
