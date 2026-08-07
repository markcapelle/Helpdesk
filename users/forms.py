from django import forms
from django.contrib.auth.models import User, Group
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    COUNTRY_CODES = [
        ("+353", "Ireland (+353)"),
        ("+44", "UK (+44)"),
        ("+1", "USA (+1)"),
        ("+49", "Germany (+49)"),
        ("+33", "France (+33)"),
    ]

    country_code = forms.ChoiceField(
        label="Country Code",
        choices=COUNTRY_CODES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    phone = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "85 123 4567"
        })
    )

    avatar = forms.FileField(
        label="Avatar",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = UserProfile
        fields = ["country_code", "phone", "avatar"]

    def clean_phone(self):
        return self.cleaned_data["phone"].strip()

    def clean(self):
        return super().clean()






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
    COUNTRY_CODES = [
        ("+353", "Ireland (+353)"),
        ("+44", "UK (+44)"),
        ("+1", "USA (+1)"),
        ("+49", "Germany (+49)"),
        ("+33", "France (+33)"),
    ]

    country_code = forms.ChoiceField(
        label="Country Code",
        choices=COUNTRY_CODES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    phone = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "85 123 4567"
        })
    )

    avatar = forms.FileField(
        label="Avatar",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = UserProfile
        fields = ["country_code", "phone", "avatar", "role"]

    def clean_phone(self):
        return self.cleaned_data["phone"].strip()

    def clean(self):
        return super().clean()



class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
