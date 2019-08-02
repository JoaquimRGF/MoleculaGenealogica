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

    pessoa_um = serializers.ReadOnlyField(source='pessoa_um.name')
    pessoa_dois = serializers.ReadOnlyField(source='pessoa_dois.name')

    class Meta:
        model = Uniao
        fields = [
            'id',
            'pessoa_um',
            'pessoa_dois'
        ]



class FamiliaSerializer(serializers.ModelSerializer):
    uniao = serializers.ReadOnlyField(source='uniao.__str__')
    filhos = PessoaSerializer(many=True)

    class Meta:
        model = Familia
        fields = [
            'id',
            'uniao',
            'filhos'
            ]
