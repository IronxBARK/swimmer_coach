from django import forms
from hfpython import swimclub  # Assuming swimdata is a module with get_data function

class FileNameForm(forms.Form):
    swimmer_name = forms.ChoiceField(
        label="Select a swimmer",
        required=True,
        choices=[],  # Placeholder, dynamically set in __init__
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['swimmer_name'].choices = [('', '--- Select ---')] + [
            (key, key) for key in swimclub.get_data().keys()
        ]

class SwimmerChoiceForm(forms.Form):
    choice = forms.ChoiceField(
        label="Select swimmer data",
        required=True,
        choices=[],  # Placeholder, dynamically set in the view
        widget=forms.Select(attrs={'class': 'form-control'})
    )
