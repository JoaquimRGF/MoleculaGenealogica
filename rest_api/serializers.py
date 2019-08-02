from rest_framework import serializers
from .models import Pessoa, Uniao, Familia





class PessoaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pessoa
        fields = [
            'id',
            'name'
            ]


class PessoaSpousesSerializer(serializers.Serializer):
    pessoa = PessoaSerializer()
    data_inicio = serializers.DateField()
    data_final = serializers.DateField()

class PessoaDescendentesSerializer(serializers.Serializer):    
    # pessoa = PessoaSerializer()
    descendentes = PessoaSerializer(many = True)


class UniaoSerializer(serializers.ModelSerializer):

    pessoa_um = serializers.PrimaryKeyRelatedField(queryset=Pessoa.objects.all())
    pessoa_dois = serializers.PrimaryKeyRelatedField(queryset=Pessoa.objects.all(), allow_null=True)

    class Meta:
        model = Uniao
        fields = [
            'id',
            'pessoa_um',
            'pessoa_dois', 
            'data_inicio', 
            'data_final'
        ]

class UniaoSerializerList(serializers.ModelSerializer):

    pessoa_um = PessoaSerializer()
    pessoa_dois = PessoaSerializer(allow_null=True)

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



class FamiliaSerializerList(serializers.ModelSerializer):
    uniao = UniaoSerializerList()
    filhos = PessoaSerializer(many=True)

    class Meta:
        model = Familia
        fields = [
            'id',
            'uniao',
            'filhos'
            ]
