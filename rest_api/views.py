from django.shortcuts import render
from rest_framework import viewsets
from .models import Pessoa, Uniao, Familia
from .serializers import PessoaSerializer, UniaoSerializer, UniaoSerializerList, FamiliaSerializer, FamiliaSerializerList

# Create your views here.
class PessoaView(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer




class UniaoView(viewsets.ModelViewSet):
    queryset = Uniao.objects.all()
    # serializer_class = UniaoSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return UniaoSerializerList
        if self.action == 'retrieve':
            return UniaoSerializerList
        return UniaoSerializer # default for create/destroy/update.


class FamiliaView(viewsets.ModelViewSet):
    queryset = Familia.objects.all()
    # serializer_class = FamiliaSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return FamiliaSerializerList
        if self.action == 'retrieve':
            return FamiliaSerializerList
        return FamiliaSerializer # default for create/destroy/update.
