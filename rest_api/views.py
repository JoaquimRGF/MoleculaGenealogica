from django.shortcuts import render
from rest_framework import viewsets
from .models import Pessoa, Uniao, Familia
from .serializers import PessoaSerializer, UniaoSerializer, FamiliaSerializer

# Create your views here.
class PessoaView(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer


class UniaoView(viewsets.ModelViewSet):
    queryset = Uniao.objects.all()
    serializer_class = UniaoSerializer


class FamiliaView(viewsets.ModelViewSet):
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializer
