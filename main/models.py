from django.db import models

class Tipo(models.Model):
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    descricao = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return f'{self.descricao}'

class Concurso(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.DateField(null=False, blank=False)
    descricao = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self) -> str:
        return f'{self.id}'

class Prova(models.Model):
    id = models.BigAutoField(primary_key=True)
    concurso = models.ForeignKey(Concurso, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Examinador(models.Model):
    nome = models.CharField(max_length=100, db_index=True, null=False, blank=False)

    def __str__(self):
        return self.nome

class Candidato(models.Model):
    nome = models.CharField(max_length=100, db_index=True, null=False, blank=False)
    habilitado = models.BooleanField(null=True)

    def __str__(self):
        return self.nome

class Avaliacao(models.Model):
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    data = models.DateField(null=False, blank=False)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    avaliacao = models.ManyToManyField(Examinador)