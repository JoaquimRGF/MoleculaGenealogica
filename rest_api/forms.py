from django import forms
from .models import Person, Union, Family


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['name']


class UnionForm(forms.ModelForm):

    class Meta:
        model = Union
        fields = [
            'person_one',
            'person_two'
        ]


class FamilyForm(forms.ModelForm):

    class Meta:
        model = Family
        fields = [
            'union',
            'children',
        ]
