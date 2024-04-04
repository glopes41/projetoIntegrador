from django.db import models

class Pesos(models.Model):
    nome = models.CharField(max_length=100)
    peso = models.DecimalField(max_digits=5, decimal_places=2)

class Notas(models.Model):
    candidato = models.CharField(max_length=100, db_index=True)
    examinador_1 = models.DecimalField(max_digits=5, decimal_places=2)
    examinador_2 = models.DecimalField(max_digits=5, decimal_places=2)
    examinador_3 = models.DecimalField(max_digits=5, decimal_places=2)
    examinador_4 = models.DecimalField(max_digits=5, decimal_places=2)
    examinador_5 = models.DecimalField(max_digits=5, decimal_places=2)
    prova = models.ForeignKey(Pesos, null=False, on_delete=models.CASCADE )