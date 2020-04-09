from django import forms
from .models import Request, Domain, Response


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


class LinkReferralForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["referral_id"]
        widgets = {
            "referral_id": forms.TextInput(
                attrs={"class": "form-control", "required": True}
            )
        }


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ["request", "created_by", "status", "note"]
        widgets = {
            "request": forms.TextInput(attrs={"class": "form-control"}),
            "created_by": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.TextInput(attrs={"class": "form-control"}),
            "note": forms.Textarea(attrs={"class": "form-control", "required": True}),
        }
