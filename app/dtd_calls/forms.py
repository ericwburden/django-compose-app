from django import forms
from .models import Call, Domain


class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain
        fields = [
            "domain",
        ]
        widgets = {
            "domain": forms.Select(attrs={"class": "form-control", "required": True})
        }


CallDomainFormset = forms.models.inlineformset_factory(
    Call, Domain, form=DomainForm, extra=1, can_delete=False
)


class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = [
            "started_at",
            "ended_at",
            "call_type",
            "caller_number",
            "caller_email",
            "caller_name",
            "caller_address",
            "caller_city",
            "caller_state",
            "caller_zip",
            "caller_age",
            "caller_gender",
            "caller_household_size",
            "covid_related",
            "client_referred",
            "referral_id",
            "referred_agency",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super(CallForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class UpdateCallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = [
            "caller_number",
            "caller_zip",
            "call_type",
            "covid_related",
            "client_referred",
            "referral_id",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super(UpdateCallForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
