from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Pessoa, Uniao, Familia
from .serializers import PessoaSerializer, UniaoSerializer, UniaoSerializerList, FamiliaSerializer, FamiliaSerializerList, PessoaSpousesSerializer, PessoaDescendentesSerializer

# Create your views here.
class PessoaView(viewsets.ModelViewSet):
    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer


@api_view(["GET"])
def spouses(request, pk):
    pessoa = get_object_or_404(Pessoa, id=pk)
    queryset = pessoa.spouses()
    print(queryset)
    spouses_serializer = list(map(lambda x: PessoaSpousesSerializer(x).data, queryset))
    print(spouses_serializer)
    return Response(spouses_serializer)


@api_view(["GET"])
def descendentes(request, pk):
    pessoa = get_object_or_404(Pessoa, id=pk)
    queryset = pessoa.descendentes()
    descendentes_serializer = PessoaDescendentesSerializer(queryset).data['descendentes']
    print(descendentes_serializer)
    
    return Response(descendentes_serializer)





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


