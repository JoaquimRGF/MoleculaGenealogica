from django.shortcuts import render, HttpResponse
from django.views import View

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Person, Union, Family
from .serializers import PersonSerializer, UnionSerializer, FamilySerializer, LinksSerializer


# Create your views here.

class PersonView(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class UnionView(viewsets.ModelViewSet):
    queryset = Union.objects.all()
    serializer_class = UnionSerializer

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class FamilyView(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class LinksView(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = LinksSerializer

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class Molecula(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(render(request, "rest_api/index.html"))
