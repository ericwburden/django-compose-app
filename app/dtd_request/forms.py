from django import forms
from .models import Request


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            "contact",
            "email",
            "primary_phone",
            "secondary_phone",
            "type_of_need",
            "add_info",
            "confirmation_code",
        ]


class MyRequestSearchForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["primary_phone", "confirmation_code"]
