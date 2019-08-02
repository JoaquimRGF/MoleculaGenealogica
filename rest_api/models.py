from django.db import models
from django.utils import timezone

# Create your models here.
class Pessoa(models.Model):
    name = models.CharField(max_length=100)
    data_criacao = models.DateTimeField( auto_now_add=True)
    data_modificacao = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.name

    def spouses(self):
        a = [{"pessoa":m.pessoa_dois, "data_inicio": m.data_inicio, "data_final": m.data_final} for m in self.pessoa_um_de.all()]
        b = [{"pessoa":m.pessoa_um, "data_inicio": m.data_inicio, "data_final": m.data_final} for m in self.pessoa_dois_de.all()]
        return a + b



class Uniao(models.Model):
    pessoa_um = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='pessoa_um_de')
    pessoa_dois = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='pessoa_dois_de', blank = True, null = True)
    data_criacao = models.DateTimeField( auto_now_add=True)
    data_modificacao = models.DateTimeField( auto_now=True)
    data_inicio = models.DateField(default="1900-01-01")
    data_final = models.DateField(default="2900-01-01")

    def __str__(self):
        return '{} + {}'.format(self.pessoa_um, self.pessoa_dois)

class Familia(models.Model):
    uniao = models.ForeignKey(Uniao, on_delete=models.CASCADE, related_name="uniao_de")
    filhos = models.ManyToManyField(Pessoa)
    data_criacao = models.DateTimeField( auto_now_add=True)
    data_modificacao = models.DateTimeField( auto_now=True)

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
