from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Candidato, Examinador, Tipo, Prova
from .forms import ProvaForm

class CadastroCandidatosList(ListView):
    model = Candidato
    
class CadastroCandidatosCreate(CreateView):
    model = Candidato
    fields = ["nome"]
    success_url = reverse_lazy("candidato_form")

class CadastroCandidatoUpdate(UpdateView):
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

class CadastroExaminadorUpdate(UpdateView):
    model = Examinador
    fields =  ["nome"]
    success_url = reverse_lazy("examinador_list")

class CadastroExaminadorDelete(DeleteView):
    model = Examinador
    fields = ["nome"]
    success_url = reverse_lazy("examinador_list")

class CadastroTipoList(ListView):
    model = Tipo

class CadastroTipoCreate(CreateView):
    model = Tipo
    fields = ["descricao", "peso"]
    success_url = reverse_lazy("tipo_form")

class CadastroTipoUpdate(UpdateView):
    model = Tipo
    fields =  ["descricao", "peso"]
    success_url = reverse_lazy("tipo_list")

class CadastroTipoDelete(DeleteView):
    model = Tipo
    fields = ["descricao", "peso"]
    success_url = reverse_lazy("tipo_list")

class CadastroProvaList(ListView):
    model = Prova

class CadastroProvaCreate(CreateView):
    model = Prova
    form_class = ProvaForm
    success_url = reverse_lazy("prova_form")

class CadastroProvaUpdate(UpdateView):
    model = Prova
    fields =  ["tipo", "concurso"]
    success_url = reverse_lazy("prova_list")

class CadastroProvaDelete(DeleteView):
    model = Prova
    fields = ["tipo", "concurso"]
    success_url = reverse_lazy("prova_list")