from django.shortcuts import render
from django.views.generic.edit import FormView
from main import forms

class ViewCadastroCandidatos(FormView):
    template_name = "cadastroCandidatos.html"
    form_class = forms.FormCandidato
    success_url = "/"