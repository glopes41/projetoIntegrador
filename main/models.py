from django.db import models

class Tipo(models.Model):
    idTipo = models.BigIntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    descricao = models.CharField(max_length=100, db_index=True)

class Prova(models.Model):
    idProva = models.AutoField(primary_key=True)
    idConcurso = models.BigIntegerField()
    tipo = models.ForeignKey(Tipo, related_name='idTipo', null=False, on_delete=models.PROTECT)

class Examinador(models.Model):
    idExaminador = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, db_index=True)

class Candidato(models.Model):
    idCandidato = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, db_index=True)
    aprovado = models.BooleanField()
    habilitado = models.BooleanField()

class Avaliacao(models.Model):
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    data = models.DateField()
    idProva = models.ForeignKey(Prova, related_name='idProva', null=False, on_delete=models.PROTECT)
    idCandidato = models.ForeignKey(Candidato, related_name='idCandidato', null=False, on_delete=models.PROTECT)
    idAvaliacao = models.ManyToManyField(Examinador, blank=False)