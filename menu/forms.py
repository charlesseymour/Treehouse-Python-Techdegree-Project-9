from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import Menu, Item, Ingredient


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = [
            'created_date',
            'season',
            'items',
            'expiration_date'
        ]
        widgets = {'created_date': forms.HiddenInput()}

    def clean(self):
        cleaned_data = super().clean()
        created = cleaned_data.get('created_date')
        expires = cleaned_data.get('expiration_date')

        if expires:
            if created >= expires:
                raise forms.ValidationError(
                    "The expiration date must be later than today.")
