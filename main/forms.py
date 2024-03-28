from django import forms

class FormCandidato(forms.Form):
    nome = forms.CharField(required=True, initial='Nome do candidato')