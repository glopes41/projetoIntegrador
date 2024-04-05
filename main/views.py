from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Candidato, Examinador, Tipo, Prova, Avaliacao, Concurso
from .forms import FormAvaliacao

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

class ConsultaMedias(ListView):
    template_name = 'medias_list.html'
    context_object_name = 'media'
    
    def get_queryset(self):
        queryset = (Candidato.objects.raw('''
            SELECT
                main_candidato.id,
                main_candidato.nome AS candidato,
                main_examinador.nome AS examinador,
                SUM(main_avaliacao.nota * main_tipo.peso)/SUM(main_tipo.peso) AS media
            FROM 
                main_candidato
            JOIN 
                main_avaliacao ON main_candidato.id = main_avaliacao.candidato_id
            JOIN 
                main_prova ON main_avaliacao.prova_id = main_prova.id
            JOIN 
                main_tipo ON main_prova.tipo_id = main_tipo.id
            JOIN 
                main_avaliacao_avaliacao ON main_avaliacao.id = main_avaliacao_avaliacao.avaliacao_id
            JOIN 
                main_examinador ON main_avaliacao_avaliacao.examinador_id = main_examinador.id
            GROUP BY 
                main_candidato.nome, main_examinador.nome;
        '''))

        return queryset
    