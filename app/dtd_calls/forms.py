from django import forms
from .models import Call, Domain, CallStatus


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
            "call_source",
            "caller_number",
            "caller_email",
            "caller_name",
            "caller_address",
            "caller_city",
            "caller_state",
            "caller_zip",
            "caller_age",
            "caller_dob",
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

        self.fields['caller_dob'].widget.attrs.update({
            'class': 'form-control datetimepicker-input',
            "data-target": "#datetimepicker1",
            "placeholder": "mm/dd/yyyy"
        })
        self.fields["caller_dob"].widget.format = "%m/%d/%Y"
        self.fields["caller_dob"].input_formats = ["%m/%d/%Y"]


class CallStatusForm(forms.ModelForm):
    class Meta:
        model = CallStatus
        fields = [
            "status",
        ]
        widgets = {
            "status": forms.Select(
                attrs={"class": "form-control call-status", "required": True}
            )
        }


CallStatusFormset = forms.models.inlineformset_factory(
    Call, CallStatus, form=CallStatusForm, extra=1, can_delete=False
)


class UpdateCallForm(forms.ModelForm):
    class Meta:
        model = Call
        fields = [
            "caller_number",
            "caller_email",
            "caller_name",
            "caller_address",
            "caller_city",
            "caller_state",
            "caller_zip",
            "caller_age",
            "caller_dob",
            "caller_gender",
            "caller_household_size",
            "covid_related",
            "client_referred",
            "referral_id",
            "referred_agency",
            "call_type",
            "notes",
            "followup_notes",
            "assigned_to",
        ]

    def __init__(self, *args, **kwargs):
        super(UpdateCallForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        self.fields['caller_dob'].widget.attrs.update({
            'class': 'form-control datetimepicker-input',
            "data-target": "#datetimepicker1",
            "placeholder": "mm/dd/yyyy"
        })
        self.fields["caller_dob"].widget.format = "%m/%d/%Y"
        self.fields["caller_dob"].input_formats = ["%m/%d/%Y"]
