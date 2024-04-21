from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Candidato, Examinador, Tipo, Prova, Avaliacao, Concurso
from .forms import FormAvaliacao
from collections import defaultdict
import json


class CandidatoListView(ListView):
    model = Candidato


class CandidatoCreateView(CreateView):
    model = Candidato
    fields = ["nome"]
    success_url = reverse_lazy("candidato_form")


class CadastroCandidatoUpdate(UpdateView):
    model = Candidato
    fields = ["nome"]
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
    fields = ["nome"]
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
    fields = ["descricao", "peso"]
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
        # Chama o método save_prova() no formulário para criar a Prova automaticamente
        prova = form.save()
        form.instance.prova = prova  # Associa a Prova à Avaliacao
        return super().form_valid(form)

    def get_success_url(self):
        # Substitua 'sucesso' pelo nome da sua URL de sucesso
        return reverse_lazy('avaliacao_form')


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
    fields = ["data", "descricao"]
    success_url = reverse_lazy("concurso_form")


class CadastroConcursoUpdate(UpdateView):
    template_name = 'concurso_form.html'
    model = Concurso
    fields = ["data", "descricao"]
    success_url = reverse_lazy("concurso_form")


class CadastroConcursoDelete(DeleteView):
    template_name = 'concurso_form.html'
    model = Concurso
    fields = ["data", "descricao"]
    success_url = reverse_lazy("concurso_form")


class ConsultaMediasCandidatos(ListView):
    template_name = 'medias_list.html'
    context_object_name = 'media'

    def get_queryset(self):
        queryset = (Candidato.objects.raw('''
            SELECT
                main_candidato.id,
                main_candidato.nome AS candidato,
                main_examinador.nome AS examinador,
                ROUND(CAST(SUM(main_avaliacao.nota * main_tipo.peso) AS FLOAT) / CAST(SUM(main_tipo.peso) AS FLOAT), 1) AS media
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


# Ordena candidatos por examinador


class OrdenaMediasExaminador(ListView):
    template_name = 'classificacao_list.html'
    context_object_name = 'classificacao'

    def get_queryset(self):
        queryset = (Candidato.objects.raw('''
            SELECT
                main_candidato.id,
                main_examinador.nome AS examinador,
                main_candidato.nome AS candidato,
                ROUND(CAST(SUM(main_avaliacao.nota * main_tipo.peso) AS FLOAT) / CAST(SUM(main_tipo.peso) AS FLOAT), 1) AS media
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
                main_examinador.nome, main_candidato.nome
            '''))

        resultados = defaultdict(dict)
        for row in queryset:
            resultados[row.examinador][row.candidato] = row.media

        # Ordena os dicionarios internos por nota
        for examinador, dicionario in resultados.items():
            resultados[examinador] = dict(
                sorted(dicionario.items(), key=lambda item: item[1], reverse=True))

        with open('primeira_ordenacao.json', 'w') as json_file:
            json.dump(resultados, json_file, indent=4)

        return resultados

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dicionario = self.get_queryset()
        lista = []
        for examinador, candidatos in dicionario.items():
            print(examinador, candidatos)
            lista.append((examinador, candidatos))
        context['lista'] = lista
        return context


class VerificaEmpateCandidatos(TemplateView):
    template_name = 'empate.html'
    success_url = reverse_lazy("empate")
    dados = defaultdict()

    def __init__(self):
        # print("ordenando.....")
        with open('primeira_ordenacao.json', 'r') as json_file:
            self.dados = json.load(json_file)
        # print(self.dados)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lista_original = self.verifica()
        empates = []
        for examinador, pares in lista_original.items():
            empates.append((examinador, pares))
        context['lista_empates'] = empates

        return context

    def verifica(self):
        pares_iguais = defaultdict(list)

        # Laço externo
        for chave_externa, valor_externo in self.dados.items():
            # Laço interno
            for chave_interna, valor_interno in valor_externo.items():
                # Laço interno para cada item
                for chave, valor in valor_externo.items():
                    if valor_interno == valor and chave_interna != chave:
                        if not pares_iguais:  # dicionario vazio
                            if (chave) and (chave_interna) not in pares_iguais[chave_externa]:
                                pares_iguais[chave_externa].append(
                                    chave_interna)
                                pares_iguais[chave_externa].append(chave)
                        else:
                            if (chave) not in pares_iguais[chave_externa]:
                                pares_iguais[chave_externa].append(
                                    chave)

        return pares_iguais

    def exibe(self):
        pares_iguais = self.verifica()
        print("Empates por examinador:")
        print(pares_iguais)
        for chave_externa, pares in pares_iguais.items():
            print(f"Examinador: '{chave_externa}':")
            for par in pares:
                print(f"  Candidatos: {par[0]} e {par[1]}")


class VerificaHabilitadosList(ListView):
    template_name = 'habilitados_list.html'
    context_object_name = 'aprovados'
    model = Candidato

    def get_queryset(self):
        queryset = super().get_queryset()
        self.calcula_medias()
        return queryset

    def calcula_medias(self):
        consulta = ConsultaMediasCandidatos()
        resultado = consulta.get_queryset()

        # Crie um dicionário para armazenar o número de médias maiores que 7 por candidato
        num_medias = defaultdict(int)
        # Itere sobre o resultado da consulta
        for row in resultado:
            # print(row.candidato, row.media)
            if float(row.media) >= 7.0:
                # print("maior")
                num_medias[row.candidato] += 1
            else:
                num_medias[row.candidato] = 0

        # Atualize os candidatos correspondentes na base de dados
        for candidato, count in num_medias.items():
            # print(count)
            if count >= 3:
                Candidato.objects.filter(
                    nome=candidato).update(habilitado=True)
                # print(f'{candidato}: {count} --> Aprovado')
            else:
                Candidato.objects.filter(
                    nome=candidato).update(habilitado=False)
                # print(f'{candidato}: {count} --> Reprovado')

        # Estruturar os resultados em um dicionário para exibição
        resultados = defaultdict(dict)
        for row in resultado:
            # print(row.candidato, row.examinador, row.media)
            resultados[row.candidato][row.examinador] = row.media

        print("items: ", resultados)
        # Ordena os dicionarios internos por nota
        for candidato, dicionario in resultados.items():
            resultados[candidato] = dict(
                sorted(dicionario.items(), key=lambda item: item[1], reverse=True))
        print(resultados)
        # Exibir os resultados
        for candidato, examinadores in resultados.items():
            print(f"Candidato: {candidato}")
            for examinador, media in examinadores.items():
                print(f"Examinador: {examinador} - Média: {media}")


# dic = {'Mateus': {'Adriano': 6.5, 'Anete': 7.6}, 'Julia': {'Adriano': 7.0, 'Anete': 8.0, 'Julia': 7.6}}
