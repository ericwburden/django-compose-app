from django import forms
from .models import Request, Domain


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = [
            "contact",
            "email",
            "primary_phone",
            "secondary_phone",
            "add_info",
            "confirmation_code",
        ]


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = [
            "domain",
        ]
        widgets = {
            "domain": forms.Select(attrs={"class": "form-control", "required": True})
        }


RequestDomainFormset = forms.models.inlineformset_factory(
    Request, Domain, form=DomainForm, extra=1, can_delete=False
)


class MyRequestSearchForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["primary_phone", "confirmation_code"]
