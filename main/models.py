from django.db import models

class Tipo(models.Model):
    idTipo = models.BigIntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    descricao = models.CharField(max_length=100, db_index=True)

class Prova(models.Model):
    idProva = models.AutoField(primary_key=True)
    idConcurso = models.BigIntegerField()
    numTipo = models.ForeignKey(Tipo, related_name='tipos', null=False, on_delete=models.PROTECT)

class Examinador(models.Model):
    idExaminador = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, db_index=True)

class Candidato(models.Model):
    idCandidato = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, db_index=True)
    aprovado = models.BooleanField()
    habilitado = models.BooleanField()

class Avaliacao(models.Model):
    idAvaliacao = models.AutoField(primary_key=True)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    data = models.DateField()
    prova = models.ForeignKey(Prova, related_name='provas', null=False, on_delete=models.PROTECT)
    numCandidato = models.ForeignKey(Candidato, related_name='candidatos', null=False, on_delete=models.PROTECT)
    numAvaliacao = models.ManyToManyField(Examinador, blank=False)