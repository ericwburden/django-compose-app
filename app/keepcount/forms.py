from .models import Counter
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class NewCounterForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = ["counter_name", "max_value"]
        widgets = {
            "counter_name": forms.TextInput(attrs={"class": "form-control"}),
            "max_value": forms.NumberInput(attrs={"class": "form-control"}),
        }


class CounterNameSearch(forms.Form):
    counter_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "CounterName"}
        )
    )

    def clean(self):
        cleaned_data = super(CounterNameSearch, self).clean()
        counter = get_object_or_404(Counter, counter_name=cleaned_data["counter_name"])
        if not counter:
            raise ValidationError("No counter with that name exists.")
