from django.db import models

class Tipo(models.Model):
    idTipo = models.AutoField(primary_key=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    descricao = models.CharField(max_length=100, db_index=True, null=False, blank=False)

class Prova(models.Model):
    idProva = models.AutoField(primary_key=True)
    idConcurso = models.BigIntegerField(null=False, blank=False)
    numTipo = models.ForeignKey(Tipo, related_name='tipos', null=False, on_delete=models.PROTECT)

class Examinador(models.Model):
    idExaminador = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, db_index=True, null=False, blank=False)

class Candidato(models.Model):
    idCandidato = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, db_index=True, null=False, blank=False)
    aprovado = models.BooleanField(null=True)
    habilitado = models.BooleanField(null=True)

class Avaliacao(models.Model):
    idAvaliacao = models.AutoField(primary_key=True)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    data = models.DateField(null=False, blank=False)
    prova = models.ForeignKey(Prova, related_name='provas', null=False, on_delete=models.PROTECT)
    numCandidato = models.ForeignKey(Candidato, related_name='candidatos', null=False, on_delete=models.PROTECT)
    numAvaliacao = models.ManyToManyField(Examinador, blank=False)