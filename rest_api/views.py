from django.shortcuts import render, HttpResponse
from django.views import View

from rest_framework import viewsets

from .models import Person, Union, Family
from .serializers import PersonSerializer, UnionSerializer, FamilySerializer, LinksSerializer


# Create your views here.

class PersonView(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class UnionView(viewsets.ModelViewSet):
    queryset = Union.objects.all()
    serializer_class = UnionSerializer


class FamilyView(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class LinksView(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = LinksSerializer


def molecula(request):
    return HttpResponse(render(request, "rest_api/index.html"))
