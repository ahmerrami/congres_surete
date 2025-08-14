from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["first_name","last_name","email","phone","nationality","institution"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Enregistrer"))
