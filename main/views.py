from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Candidato

class CadastroCandidatosList(ListView):
    model = Candidato
    
class CadastroCandidatosCreate(CreateView):
    model = Candidato
    fields = ["nome"]
    success_url = reverse_lazy("candidato_form")