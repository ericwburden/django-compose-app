from django import forms
from .models import Call


class CallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = [
            "started_at",
            "ended_at",
            "caller_number",
            "caller_zip",
            "call_type",
            "covid_related",
            "client_referred",
            "referral_id",
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
