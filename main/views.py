from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Candidato, Examinador, Tipo, Prova, Avaliacao, Concurso
from .forms import FormAvaliacao
from collections import defaultdict
from django.shortcuts import render
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
                main_candidato.nome, main_examinador.nome
            '''))

        return queryset


# Ordena candidatos por examinador


class OrdenaMediasExaminador(ListView):
    template_name = 'classificacao_list.html'
    context_object_name = 'classificacao'

    # Calcula as medias ponderadas de todos os candidatos e agrupa os candidatos por examinador
    # A consulta ja sai com os candidatos ordenados por media decrescente

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
            ORDER BY
                main_examinador.nome, media DESC
            '''))

        # Cria um dicionario com o resultado do SELECT do banco de dados
        resultados = defaultdict(dict)
        for row in queryset:
            resultados[row.examinador][row.candidato] = row.media

        # Ordena os dicionarios internos por media
        '''
        for examinador, dicionario in resultados.items():
            resultados[examinador] = dict(
                sorted(dicionario.items(), key=lambda item: item[1], reverse=True))
        '''

        # Salvamos o dicionario ordenado por medias em arquivo na pasta local
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
        # Carrega os candidatos ordenados por media de um arquivo na pasta local
        with open('primeira_ordenacao.json', 'r') as json_file:
            self.dados = json.load(json_file)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lista = self.verifica()
        dicionarios_vazios = []
        for chave, valor in lista.items():
            if not valor:
                dicionarios_vazios.append(chave)
        for chave in dicionarios_vazios:
            lista.pop(chave)
        context['dados'] = lista
        print(context)

        return context

    def verifica(self):
        empates = {}

        # Laço externo, Examinadores:
        # caso 1: empate unico { "Adriano": { "Evandro": 8.9, "Pedro": 7.3, "Maria": 7.3 } }
        # caso 2: varios empates { "Adriano": { "Evandro": 8.9, "Pedro": 7.3, "Maria": 7.3, "Jorge": 6.0, "Tiago": 6.0 } }
        for chave_externa, valor_externo in self.dados.items():
            # Laço interno, Candidatos: { "Evandro": 8.9, "Pedro": 7.3, "Maria": 7.3 }
            empates[chave_externa] = {}
            n = 1
            empates_encontrados = set()
            for chave_interna, valor_interno in valor_externo.items():
                # Laço interno para cada item
                # Conjunto do python para nao permitir elementos repetidos
                nomes_empatados = set([chave_interna])
                for chave, valor in valor_externo.items():
                    if valor_interno == valor and chave_interna != chave:
                        if chave not in nomes_empatados:
                            nomes_empatados.add(chave)
                if len(nomes_empatados) > 1:
                    if tuple(sorted(nomes_empatados)) not in empates_encontrados:
                        empates_encontrados.add(
                            tuple(sorted(nomes_empatados)))
                        # Use n como chave para cada conjunto de empates
                        empates[chave_externa][f'empate_{n}'] = sorted(
                            list(nomes_empatados))
                        n += 1
                # print(empates)

        return empates

    # Pega o retorno do template empate.html onde o usuario escolheu o desempate.

    def post(self, request, *args, **kwargs):
        # Processar os dados do formulário
        escolha_usuario = {}
        candidatos = defaultdict(dict)
        conj = set()

        # Pegamos o retorno do usuario e criamos um dicionario
        for chave, valor in request.POST.items():
            # print(chave, valor)
            lista = chave.split(',')
            if len(lista) > 2:
                examinador, empate, candidato = lista
                #print(examinador, empate, candidato)
                if examinador not in escolha_usuario:
                    escolha_usuario[examinador] = {}
                if empate not in escolha_usuario[examinador]:
                    escolha_usuario[examinador][empate] = {}
                escolha_usuario[examinador][empate][candidato] = valor
        print("Retorno do usuario como dicionario:", escolha_usuario)

        # Aqui ordenamos os candidatos conforme escolha do usuario em ordem crescente
        for examinador, empates in escolha_usuario.items():
            for empate, candidatos in empates.items():
                escolha_usuario[examinador][empate] = {chave: valor for chave, valor in sorted(
                    candidatos.items(), key=lambda item: int(item[1]))}
        print("Escolha do usuario ordenada: ", escolha_usuario)

        # Para cada examinador do dicionario de empates pegar os empates
        dic_original = self.dados
        dic_ordenado = {}
        for examinador, empates in escolha_usuario.items():
            #print(examinador)
            # Para cada empate, substituir os candidatos na ordem correta no dicionario original
            dic_candidatos = {}
            for empate, candidatos in empates.items():
                for candidato, nota in dic_original[examinador].items():
                    if candidato not in candidatos:
                        dic_candidatos[candidato] = nota
                    else:
                        dic_candidatos.update(candidatos)
                        break;
                #print("aux: ", dic_candidatos)
                #print(empate, candidatos)
            dic_ordenado[examinador] = dic_candidatos
            #print(dic_ordenado)
            #print(self.dados)
        
        # Garante a atualização das notas
        for examinador, candidatos in self.dados.items():
            if examinador not in dic_ordenado:
                dic_ordenado[examinador] = {}
            for candidato, nota in candidatos.items():
                #print(candidato, nota)
                dic_ordenado[examinador][candidato] = nota
        
        # Salvamos o dicionario ordenado em um arquivo
        with open('ordenacao_final.json', 'w') as json_file:
            json.dump(dic_ordenado, json_file, indent=4)
        #print("final: ", dic_ordenado)

            

        return render(request, 'escolha_usuario_sucesso.html', {'mensagem': 'Ordem dos candidatos escolhida com sucesso!'})


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

        # Cria um dicionário para armazenar o número de médias maiores que 7 por candidato
        num_medias = defaultdict(int)
        # Itera sobre o resultado da consulta
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
