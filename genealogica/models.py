from django.db import models


# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Family(models.Model):
    union = models.ManyToManyField(Person, related_name="union_family")
    children = models.ManyToManyField(Person, blank=True, related_name="children_family")

    def __str__(self):
        return '{} --> {}'.format([i.name for i in self.union.all()], [i.name for i in self.children.all()])

