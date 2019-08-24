from django.shortcuts import render, HttpResponse

from rest_framework import viewsets

from .models import Person, Family
from .serializers import PersonSerializer, FamilySerializer, LinksSerializer


# Create your views here.

class PersonView(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    
    
class FamilyView(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer


class LinksView(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = LinksSerializer
    
    
def molecula(request):
    return HttpResponse(render(request, "genealogica/index.html"))
