from django.db import models

# Create your models here.
class Pessoa(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Uniao(models.Model):
    pessoa_um = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='pessoa_um_de')
    pessoa_dois = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='pessoa_dois_de')

    def __str__(self):
        return '{} + {}'.format(self.pessoa_um, self.pessoa_dois)

class Familia(models.Model):
    uniao = models.ForeignKey(Uniao, on_delete=models.CASCADE)
    filhos = models.ManyToManyField(Pessoa)

    def __str__(self):
        return '{} --> {}'.format(self.uniao, self.filhos)



# from django.db import models
#
# # Create your models here.
#
# class Pessoa(models.Model):
#
#     name = models.CharField(max_length=100)
#     pai = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='pessoa_pai')
#     mae = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='pessoa_mae')
#
#     def __str__(self):
#         return self.name
#
#
#
#     # Pessoa.objects.filter(mae__name = 'Tia Anabela')
