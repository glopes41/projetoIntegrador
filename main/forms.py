from django import forms
from .models import Prova, Avaliacao

class ProvaForm(forms.ModelForm):
    class Meta:
        model = Prova
        fields = [ 'tipo', 'concurso' ]

    
class FormCandidato(forms.Form):
    nome = forms.CharField(required=True, initial='Nome do candidato')

class FormAvaliacao(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = [ 'nota' ]