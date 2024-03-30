from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Candidato

class CadastroCandidatosList(ListView):
    model = Candidato
    
class CadastroCandidatosCreate(CreateView):
    model = Candidato
    fields = ["nome"]
    success_url = reverse_lazy("candidato_form")

class CadastriCandidatoUpdate(UpdateView):
    model = Candidato
    fields =  ["nome"]
    success_url = reverse_lazy("candidato_list")

class CadastroCandidatoDelete(DeleteView):
    model = Candidato
    fields = ["nome"]
    success_url = reverse_lazy("candidato_list")