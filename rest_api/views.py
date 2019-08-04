from django.shortcuts import render
from rest_framework import viewsets
from .models import Person, Union, Family
from .serializers import PersonSerializer, UnionSerializer, UnionSerializerList, FamilySerializer, FamilySerializerList

# Create your views here.


class PersonView(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class UnionView(viewsets.ModelViewSet):
    queryset = Union.objects.all()
    serializer_class = UnionSerializer

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return UnionSerializerList
    #     if self.action == 'retrieve':
    #         return UnionSerializerList
    #     return UnionSerializer  # default for create/destroy/update.


class FamilyView(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return FamilySerializerList
    #     if self.action == 'retrieve':
    #         return FamilySerializerList
    #     return FamilySerializer # default for create/destroy/update.
