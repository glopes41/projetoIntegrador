from django.views.generic import ListView, CreateView
from .models import Candidato

class CadastroCandidatosList(ListView):
    model = Candidato

class CadastroCandidatosCreate(CreateView):
    model = Candidato
    fields = ["nome"]