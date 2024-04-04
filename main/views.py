from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Candidato, Examinador, Tipo, Prova, Avaliacao, Concurso
from django.views.generic.edit import FormView
from .forms import FormAvaliacao
from django.db.models import Sum, F

class CandidatoListView(ListView):
    model = Candidato
    paginate_by = 10
    
class CandidatoCreateView(CreateView):
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
    model = Avaliacao
    template_name = 'avaliacao_form.html'
    success_url = reverse_lazy('avaliacao_form')
    form_class = FormAvaliacao

    def form_valid(self, form):
        prova = form.save()  # Chama o método save_prova() no formulário para criar a Prova automaticamente
        form.instance.prova = prova  # Associa a Prova à Avaliacao
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('avaliacao_form')  # Substitua 'sucesso' pelo nome da sua URL de sucesso
    
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

class ConsultaAprovados(ListView):
    template_name = 'aprovados_list.html'
    context_object_name = 'media'
    
    def get_queryset(self):
        queryset = (Candidato.objects
            .annotate(candidato=F('nome'))
            .annotate(examinador=F('avaliacao__avaliacao__examinador__nome'))
            .annotate(soma_notas_peso=Sum(F('avaliacao__nota') * F('avaliacao__prova__tipo__peso')))
            .annotate(soma_pesos=Sum('avaliacao__prova__tipo__peso'))
            .annotate(media=Sum('soma_notas_peso') / Sum('soma_pesos'))
            .values('candidato', 'examinador', 'media')
            .order_by('candidato', 'examinador'))
        return queryset

