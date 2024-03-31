from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Candidato, Examinador

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

class CadastroExaminadorList(ListView):
    model = Examinador
    
class CadastroExaminadorCreate(CreateView):
    model = Examinador
    fields = ["nome"]
    success_url = reverse_lazy("examinador_form")

class CadastriExaminadorUpdate(UpdateView):
    model = Examinador
    fields =  ["nome"]
    success_url = reverse_lazy("examinador_list")

class CadastroExaminadorDelete(DeleteView):
    model = Examinador
    fields = ["nome"]
    success_url = reverse_lazy("examinador_list")