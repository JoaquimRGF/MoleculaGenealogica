from rest_framework import serializers

from .models import Person, Family


class PersonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Person
        fields = [
            'id',
            'name'
            ]


class FamilySerializer(serializers.ModelSerializer):
    union = PersonSerializer(many=True)
    children = PersonSerializer(many=True)

    class Meta:
        model = Person
        fields = [
            'id',
            'union',
            'children'
            ]

    def validate(self, attrs):
        """
        Avoid duplicate ids in union and/or children
        """
        union_id = []
        for union in attrs['union']:
            if 'id' in union.keys():
                union_id.append(union['id'])
            if len(union_id) != len(set(union_id)):
                raise serializers.ValidationError('You have duplicate union')
        children_id = []
        for children in attrs['children']:
            if 'id' in children.keys():
                children_id.append(children['id'])
            if len(children_id) != len(set(children_id)):
                raise serializers.ValidationError('You have duplicate children')
        if len(union_id + children_id) != len(set(union_id + children_id)):
            raise serializers.ValidationError('You have duplicate union and children')

        return attrs

    def validate_union(self, value):

        """
        Avoid empty union and more than two persons
        """
        if not value:
            raise serializers.ValidationError('Union cannot be empty.')
        if len(value) > 2:
            raise serializers.ValidationError('Maximum two persons are allowed.')

        """
        Avoid add union if two persons are siblings
        """
        qs = Family.objects.all()
        if len(value) == 2:
            if 'id' in value[0] and 'id' in value[1]:
                for family in qs:
                    child_id = [child.id for child in family.children.all()]
                    if value[0]['id'] in child_id and value[1]['id'] in child_id:
                        raise serializers.ValidationError('Cant union 2 siblings.')

        """
        Avoid family-union duplicate
        """
        if len(value) == 2:
            if 'id' in value[0] and 'id' in value[1]:
                if self.instance:
                    obj_id = self.instance.id
                    for family in qs.exclude(id=obj_id):
                        union_id = [union.id for union in family.union.all()]
                        if value[0]['id'] in union_id and value[1]['id'] in union_id:
                            raise serializers.ValidationError('This union already exist in family id: {}'.format(family.id))
                else:
                    for family in qs:
                        union_id = [union.id for union in family.union.all()]
                        if value[0]['id'] in union_id and value[1]['id'] in union_id:
                            raise serializers.ValidationError('This union already exist in family id: {}'.format(family.id))

        return value

    def validate_children(self, value):

        qs = Family.objects.all()

        """
        Avoid add children that exists in another family.
        """
        for child_request in value:
            if 'id' in child_request.keys():
                if self.instance:
                    obj_id = self.instance.id
                    for family in qs.exclude(id=obj_id):
                        child_id = [child.id for child in family.children.all()]
                        if child_request['id'] in child_id:
                            raise serializers.ValidationError(
                                'Child with the id: {} is child in family with the '
                                'id: {}.'.format(child_request['id'], family.id))
                else:
                    for family in qs:
                        child_id = [child.id for child in family.children.all()]
                        if child_request['id'] in child_id:
                            raise serializers.ValidationError(
                                'Child with the id: {} is child in family with the '
                                'id: {}.'.format(child_request['id'], family.id))
            else:
                continue

        return value

    def create(self, validated_data):

        """
        Create a family, get a person if a id exists or create a new one.
        """

        union_data = validated_data.pop('union')
        children_data = validated_data.pop('children')

        family = Family()
        family.save()

        for uni in union_data:
            if 'id' in uni.keys():
                obj = Person.objects.get(id=uni["id"])
                family.union.add(obj)
            else:
                obj = Person.objects.create(**uni)
                family.union.add(obj)

        for child in children_data:
            if 'id' in child.keys():
                obj = Person.objects.get(id=child["id"])
                family.children.add(obj)
            else:
                obj = Person.objects.create(**child)
                family.children.add(obj)

        return family

    def update(self, instance, validated_data):

        """
        Update Family instance, get a person if a id exists or create a new one.
        """

        union_data = validated_data.pop('union')
        children_data = validated_data.pop('children')

        keep_union = []
        for uni in union_data:
            if "id" in uni.keys():
                u = Person.objects.get(id=uni["id"])
                keep_union.append(u)

            else:
                u = Person.objects.create(**uni)
                keep_union.append(u)

        instance.union.set(keep_union)

        keep_children = []
        for child in children_data:
            if "id" in child.keys():
                c = Person.objects.get(id=child["id"])
                keep_children.append(c)

            else:
                c = Person.objects.create(**child)
                keep_children.append(c)

        instance.children.set(keep_children)

        return instance


class LinksSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Family
        fields = [
            'data',
        ]

    def get_data(self, obj):

        data = []

        data.append({
            "source": obj.union.all()[0].id,
            "target": obj.union.all()[1].id,
            "type": "union",
        })

        data.append({
            "source": obj.union.all()[1].id,
            "target": obj.union.all()[0].id,
            "type": "union",
        })

        for child in obj.children.all():
            data.append({
                        "source": obj.union.all()[0].id,
                        "target": child.id,
                        "type": "children",
                        })
            data.append({
                        "source": obj.union.all()[1].id,
                        "target": child.id,
                        "type": "children",
                        })
        
        return data
