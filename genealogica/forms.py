from django import forms
from django.core.exceptions import ValidationError
from .models import Person, Family


class PersonForm(forms.ModelForm):
    model = Person
    fields = [
        'name',
    ]
    

class FamilyForm(forms.ModelForm):

    class Meta:
        model = Family
        fields = [
            'union',
            'children'
        ]

    def clean(self):
        union = self.cleaned_data.get('union')
        if not union:
            raise ValidationError('Union cannot be empty.')
        if union.count() > 2:
            raise ValidationError('Maximum two persons are allowed.')

        return self.cleaned_data
