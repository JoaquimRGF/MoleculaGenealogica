from rest_framework import serializers
from .models import Person, Union, Family


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = [
            'id',
            'name'
            ]
        extra_kwargs = {
            'name': {'validators': []},
        }


class UnionSerializer(serializers.ModelSerializer):

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
        person_one_obj = Person.objects.get_or_create(**person_one)

        person_two = validated_data['person_two']
        person_two_obj = Person.objects.get_or_create(**person_two)

        union = Union.objects.get_or_create(person_one=person_one_obj[0], person_two=person_two_obj[0])

        return union[0]


class FamilySerializer(serializers.ModelSerializer):

    union = UnionSerializer()
    children = PersonSerializer(many=True)

    class Meta:
        model = Family
        fields = [
            'id',
            'union',
            'children'
            ]

    def create(self, validated_data):

        union = validated_data['union']
        children = validated_data['children']

        person_one_obj = Person.objects.get_or_create(**union['person_one'])
        person_two_obj = Person.objects.get_or_create(**union['person_two'])

        union = Union.objects.get_or_create(person_one=person_one_obj[0], person_two=person_two_obj[0])

        family = Family(union=union[0])
        family.save()

        for child in children:
            obj = Person.objects.get_or_create(**child)
            family.children.add(obj[0])

        return family


class LinksSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Family
        fields = [
            'data',
        ]

    def get_data(self, obj):

        data = []

        if obj.union.person_two is not None:
            data.append({
                "source": obj.union.person_one.id,
                "target": obj.union.person_two.id,
                "type": "union",
                "strength": 1
            })

            for chil in obj.children.all():
                data.append({
                    "source": obj.union.person_one.id,
                    "target": chil.id,
                    "type": "children",
                    "strength": 0.5
                })
                data.append({
                    "source": obj.union.person_two.id,
                    "target": chil.id,
                    "type": "children",
                    "strength": 0.5
                })

        else:
            for chil in obj.children.all():
                data.append({
                    "source": obj.union.person_one.id,
                    "target": chil.id,
                    "type": "children",
                    "strength": 0.5
                })
        return data
