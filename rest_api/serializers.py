from rest_framework import serializers
from .models import Pessoa, Uniao, Familia

class PessoaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = [
            'id',
            'name'
            ]

class UniaoSerializer(serializers.ModelSerializer):

    pessoa_um = serializers.PrimaryKeyRelatedField(queryset=Pessoa.objects.all())
    pessoa_dois = serializers.PrimaryKeyRelatedField(queryset=Pessoa.objects.all())

    class Meta:
        model = Uniao
        fields = [
            'id',
            'pessoa_um',
            'pessoa_dois', 
            'data_inicio', 
            'data_final'
        ]



class FamiliaSerializer(serializers.ModelSerializer):
    uniao = serializers.PrimaryKeyRelatedField(queryset=Uniao.objects.all())
    filhos = serializers.PrimaryKeyRelatedField(queryset=Pessoa.objects.all(), many=True)

    class Meta:
        model = Familia
        fields = [
            'id',
            'uniao',
            'filhos'
            ]
