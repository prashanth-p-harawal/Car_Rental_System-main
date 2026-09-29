from django import forms
from .models import Car, Booking

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "brand": forms.TextInput(attrs={"class": "form-control"}),
            "model": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "fuel": forms.Select(attrs={"class": "form-select"}),
            "transmission": forms.Select(attrs={"class": "form-select"}),
            "seats": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            "full_name",
            "email",
            "phone",
            "pickup_date",
            "return_date",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "pickup_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            "return_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]