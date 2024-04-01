from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Candidato, Examinador, Tipo, Prova, Avaliacao, Concurso
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
    template_name = 'prova_list.html'
    model = Prova

class CadastroProvaCreate(CreateView):
    template_name = 'prova_form.html'
    model = Prova
    fields = ["tipo", "concurso"]
    success_url = reverse_lazy("prova_form")

class CadastroProvaUpdate(UpdateView):
    template_name = 'prova_form.html'
    model = Prova
    fields =  ["tipo", "concurso"]
    success_url = reverse_lazy("prova_list")

class CadastroProvaDelete(DeleteView):
    template_name = 'prova_confirm_delete.html'
    model = Prova
    fields = ["tipo", "concurso"]
    success_url = reverse_lazy("prova_list")

class CadastroAvaliacaoList(ListView):
    template_name = 'avaliacao_list.html'
    model = Avaliacao
    
class CadastroAvaliacaoCreate(CreateView):
    template_name = 'avaliacao_form.html'
    model = Avaliacao
    fields = ["nota", "data", "prova", "candidato", "avaliacao"]
    success_url = reverse_lazy("avaliacao_form")

class CadastroAvaliacaoUpdate(UpdateView):
    template_name = 'avaliacao_form.html'
    model = Avaliacao
    
    fields = ["nota", "data", "prova", "candidato"]
    success_url = reverse_lazy("avaliacao_list")

class CadastroAvaliacaoDelete(DeleteView):
    template_name = 'avaliacao_confirm_delete.html'
    model = Avaliacao
    fields = ["nota", "data", "prova", "candidato"]
    success_url = reverse_lazy("avaliacao_list")

class CadastroConcursoList(ListView):
    template_name = 'concurso_list.html'
    model = Concurso
    
class CadastroConcursoCreate(CreateView):
    template_name = 'concurso_form.html'
    model = Concurso
    fields = [ "data", "descricao"]
    success_url = reverse_lazy("concurso_form")

class CadastroConcursoUpdate(UpdateView):
    template_name = 'concurso_form.html'
    model = Concurso
    fields = [ "data", "descricao"]
    success_url = reverse_lazy("concurso_form")

class CadastroConcursoDelete(DeleteView):
    template_name = 'concurso_form.html'
    model = Concurso
    fields = [ "data", "descricao"]
    success_url = reverse_lazy("concurso_form")