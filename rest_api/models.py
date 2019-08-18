from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Union(models.Model):
    person_one = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_one_related')
    person_two = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_two_related', null=True)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} and {}'.format(self.person_one, self.person_two)


class Family(models.Model):
    union = models.ForeignKey(Union, on_delete=models.CASCADE)
    children = models.ManyToManyField(Person, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} --> {}'.format(self.union, tuple(i.name for i in self.children.all()))
