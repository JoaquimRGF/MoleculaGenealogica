from rest_framework import serializers
from .models import Person, Union, Family


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = [
            'id',
            'name'
            ]


class UnionSerializer(serializers.ModelSerializer):

    # person_one = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())
    # person_two = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), allow_null=True)

    person_one = PersonSerializer()
    person_two = PersonSerializer(allow_null=True)

    class Meta:
        model = Union
        fields = [
            'id',
            'person_one',
            'person_two',
        ]

    def create(self, validated_data):
        person_one = validated_data['person_one']
        person_one_obj = Person.objects.create(**person_one)

        person_two = validated_data['person_two']
        person_two_obj = Person.objects.create(**person_two)

        union = Union.objects.create(person_one=person_one_obj, person_two=person_two_obj)

        return union


class UnionSerializerList(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    person_one = PersonSerializer()
    person_two = PersonSerializer(allow_null=True)

    class Meta:
        model = Union
        fields = [
            'id',
            'person_one',
            'person_two',
        ]


class FamilySerializer(serializers.ModelSerializer):

    # union = serializers.PrimaryKeyRelatedField(queryset=Union.objects.all())
    # children = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), many=True)

    union = UnionSerializerList()
    children = PersonSerializer(many=True)

    class Meta:
        model = Family
        fields = [
            'id',
            'union',
            'children'
            ]


class FamilySerializerList(serializers.ModelSerializer):
    union = UnionSerializerList()
    children = PersonSerializer(many=True)

    class Meta:
        model = Family
        fields = [
            'id',
            'union',
            'children'
            ]

    # def create(self, validated_data):
    #
    #     union = validated_data.pop('union')
    #     children = validated_data.pop('children')
    #     id = Family.objects.create(**validated_data)
    #
    #     Person.objects.create(**union['person_one'])
    #     Person.objects.create(**union['person_two'])
    #
    #     for child in children:
    #         Person.objects.create(**child)
    #
    #     return id

