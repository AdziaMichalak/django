from django import forms
from maths.models import Result

OPERATION_CHOICES = [
    ("add", "add"),
    ("sub", "sub"),
    ("mul", "mul"),
    ("div", "div"),
]


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        value = cleaned_data.get('value')
        error = cleaned_data.get('error')

        if value and error:
            raise forms.ValidationError("Podaj tylko jedną z wartości")
        elif not (value or error):
            raise forms.ValidationError("Nie podano żadnej wartości!")


class SearchForm(forms.Form):
    operation = forms.ChoiceField(label='Operacja', choices=OPERATION_CHOICES)

