from django import forms
from .models import Prova, Tipo

class ProvaForm(forms.ModelForm):
    tipo = forms.IntegerField(required=True)
    concurso = forms.IntegerField(required=True)

    class Meta:
        model = Prova
        fields = [ 'tipo', 'concurso' ]


class FormCandidato(forms.Form):
    nome = forms.CharField(required=True, initial='Nome do candidato')