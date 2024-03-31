from django.db import models

class Tipo(models.Model):
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    descricao = models.CharField(max_length=100, db_index=True)

class Prova(models.Model):
    concurso = models.BigIntegerField(null=False, blank=False)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)

class Examinador(models.Model):
    nome = models.CharField(max_length=100, db_index=True, null=False, blank=False)

class Candidato(models.Model):
    nome = models.CharField(max_length=100, db_index=True, null=False, blank=False)
    aprovado = models.BooleanField(null=True)
    habilitado = models.BooleanField(null=True)

class Avaliacao(models.Model):
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    data = models.DateField(null=False, blank=False)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    avaliacao = models.ManyToManyField(Examinador)