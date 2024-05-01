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
        if request.POST.items():  # Se não houver empates
            print("Dicionario vazio")
            # Garante a atualização das notas
            dic_ordenado = {}
            for examinador, candidatos in self.dados.items():
                if examinador not in dic_ordenado:
                    dic_ordenado[examinador] = {}
                for candidato, nota in candidatos.items():
                    # print(candidato, nota)
                    dic_ordenado[examinador][candidato] = nota

            # Salvamos o dicionario ordenado em um arquivo
            with open('ordenacao_final.json', 'w') as json_file:
                json.dump(dic_ordenado, json_file, indent=4)
            # print("final: ", dic_ordenado)
            return render(request, 'index.html')

        else:
            # Pegamos o retorno do usuario e criamos um dicionario
            for chave, valor in request.POST.items():
                # print(chave, valor)
                lista = chave.split(',')
                if len(lista) > 2:
                    examinador, empate, candidato = lista
                    # print(examinador, empate, candidato)
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
                # print(examinador)
                # Para cada empate, substituir os candidatos na ordem correta no dicionario original
                dic_candidatos = {}
                for empate, candidatos in empates.items():
                    for candidato, nota in dic_original[examinador].items():
                        if candidato not in candidatos:
                            dic_candidatos[candidato] = nota
                        else:
                            dic_candidatos.update(candidatos)
                            break
                    # print("aux: ", dic_candidatos)
                    # print(empate, candidatos)
                dic_ordenado[examinador] = dic_candidatos
                # print(dic_ordenado)
                # print(self.dados)

            # Garante a atualização das notas
            for examinador, candidatos in self.dados.items():
                if examinador not in dic_ordenado:
                    dic_ordenado[examinador] = {}
                for candidato, nota in candidatos.items():
                    # print(candidato, nota)
                    dic_ordenado[examinador][candidato] = nota

            # Salvamos o dicionario ordenado em um arquivo
            with open('ordenacao_final.json', 'w') as json_file:
                json.dump(dic_ordenado, json_file, indent=4)
            # print("final: ", dic_ordenado)

            return render(request, 'escolha_usuario_sucesso.html', {'mensagem': 'Ordem dos candidatos escolhida com sucesso!'})

# Classe para a classificação final dos candidatos


class ClassificacaoFinalList(ListView):
    template_name = 'classificacao_final_list.html'
    model = Candidato
    num_habilitados = 0
    candidatos_habilitados = []
    dicionario_ordenado = {}

    def __init__(self):
        self.num_habilitados = Candidato.objects.filter(
            habilitado=True).count()
        candidatos_habilitados = Candidato.objects.filter(habilitado=True)
        for candidato in candidatos_habilitados:
            self.candidatos_habilitados.append(candidato.nome)

        with open('ordenacao_final.json', 'r') as arq:
            ordenados = json.load(arq)

        self.dicionario_ordenado = {chave: list(valores.keys())
                                    for chave, valores in ordenados.items()}
        self.calcula_classificacao_final()

    def calcula_classificacao_final(self):
        acumulador = 0
        empate_com_duas_indicacoes = []
        classificacao_final = {}

        print("num_habilitados: ", self.num_habilitados)
        for posicao in range(self.num_habilitados):
            for candidato in self.candidatos_habilitados:
                print(self.dicionario_ordenado)
                for chave, valores in self.dicionario_ordenado.items():
                    if candidato == valores[0]:
                        acumulador += 1

                if acumulador >= 3:
                    # adiciona ao dicionário de classificação final o candidato classificado e o nº de indicações
                    classificacao_final[candidato] = acumulador
                    # reinicia o acumulador para contagem das indicações da próxima posição
                    acumulador = 0
                    # zera duas indicações que possam ter acontecido antes da classificação do 1º colocado, para não cair no 'len(empate_com_duas_indicacoes) == 1'
                    empate_com_duas_indicacoes = []
                    # retira das listas de habilitados o candidato já classificado
                    for chave, valores in self.dicionario_ordenado.items():
                        if candidato in valores:
                            valores.remove(candidato)
                    break

                # se houver 2 indicações, ainda é necessário iterar os candidatos até o fim, para ver se não há outro com 2 indicações
                if acumulador == 2:
                    empate_com_duas_indicacoes.append(candidato)
                    acumulador = 0

                # zera o acumulador para a próxima iteração, caso o candidato tenha uma única indicação e, assim, não entre em nenhum 'if' anterior
                if acumulador == 1:
                    acumulador = 0

            # caso ninguém tenha vencido com 3 indicações, verifica se há uma só pessoa com 2 indicações, a qual venceria os outros cada um com apenas 1 indicação
            if len(empate_com_duas_indicacoes) == 1:
                # adiciona ao dicionário de classificação final o candidato classificado com 2 indicações
                classificacao_final[empate_com_duas_indicacoes[0]] = 2
                # retira das listas de habilitados o candidato já classificado
                for chave, valores in self.dicionario_ordenado.items():
                    if empate_com_duas_indicacoes[0] in valores:
                        valores.remove(empate_com_duas_indicacoes[0])

            # verifica se houve empate de indicações
            if len(empate_com_duas_indicacoes) == 2:

                # CÓDIGO PROVISÓRIO!!!!

                # coloca o primeiro que teve 2 indicações como o próximo na classificação
                classificacao_final[empate_com_duas_indicacoes[0]] = 2
                # retira das listas de habilitados o candidato classificado
                for chave, valores in self.dicionario_ordenado.items():
                    if empate_com_duas_indicacoes[0] in valores:
                        valores.remove(empate_com_duas_indicacoes[0])
                # zera a lista de empate
                empate_com_duas_indicacoes = []

                # PRÉVIA DO CÓDIGO DEFINITIVO
                '''
                # pressuposto: haver outro atributo da entidade 'prova', que é a 'precedência' para fins de desempate (int: 0,1,...), cadastrada junto com o tipo e o peso
                
                provas_para_desempate = 'fazer um list de strings com o nome das provas com o atributo precedência diferente de 0, ordenadas segundo o número da precedência'
                #iteração sobre as provas
                for prova in provas_para_desempate:
                    #aqui se faz um SELECT para calcular a media aritmetica na prova da iteração atual
                    #formula desta media: (nota do examinador 1 + ... + nota do examiandor 5)/5
                    #coloca-se a media no dicionário abaixo
                    #lembrando que a lista 'empate_com_duas_indicacoes' contém os 2 empatados
                    media = {empate_com_duas_indicacoes[0]: SELECT da media1, empate_com_duas_indicacoes[1]: SELECT da media2}
                    
                    # Verifica se a media atual já desempata
                    if media[empate_com_duas_indicacoes[0]] != media[empate_com_duas_indicacoes[1]]:
                        # Ordena os empatados pela maior media na prova da iteração atual
                        empate_com_duas_indicacoes.sort(key=lambda x: media[x], reverse=True)
                        #coloca o primeiro como o próximo na classificação
                        classificacao_final[empate_com_duas_indicacoes[0]] = 2
                        #retira das listas de habilitados o candidato classificado
                        for chave, valores in dicionario_ordenado.items():
                            if empate_com_duas_indicacoes[0] in valores:
                                valores.remove(empate_com_duas_indicacoes[0])
                        #zera a lista de empate
                        empate_com_duas_indicacoes = []
                        break #isto para parar de percorrer as provas, visto que o desempate acabou
                
                #se nenhuma prova desempatou, vai para a escolha do usuário. Aqui viria esse código
                #if len(empate_com_duas_indicacoes) != 0:
                    #colocar aqui a escolha do usuário
                    
                '''

            # verifica se todos os candidatos empataram com 1 indicação
            if len(classificacao_final) == posicao:
                # CÓDIGO PROVISÓRIO!!!!

                # coloca qualquer um na classificação
                for candidato in self.candidatos_habilitados:

                    for chave, valores in self.dicionario_ordenado.items():
                        if valores:
                            if candidato == valores[0]:
                                classificacao_final[candidato] = 1
                                break

                    for chave, valores in self.dicionario_ordenado.items():
                        if candidato in valores:
                            valores.remove(candidato)
                    break

            # PRÉVIA DO CÓDIGO DEFINITIVO

                '''
                # pressuposto: haver outro atributo da entidade 'prova', que é a 'precedência' para fins de desempate (int: 0,1,...), cadastrada junto com o tipo e o peso
                
                provas_para_desempate = 'fazer um list de strings com o nome das provas com o atributo precedência diferente de 0, ordenadas segundo o número da precedência'
                #iteração sobre as provas
                for prova in provas_para_desempate:
                    if len(classificacao_final) == posicao: #isto para não iterar, caso a classificação saia aqui dentro 
                        #aqui se faz um SELECT para calcular a media artimetica na prova da iteração atual
                        #formula desta media: (nota do examinador 1 + ... + nota do examiandor 5)/5
                        #coloca-se a media no dicionário abaixo
                        media = {}
                        for candidato in candidatos_habilitados:
                            media[candidato] = #media do candidato
                        
                        # Verifica se a media atual já desempata
                        for candidato in candidatos_habilitados:
                            vence_todos = True
                            for outro_candidato in candidatos_habilitados:
                                if candidato != outro_candidato and media[candidato] <= media[outro_candidato]:
                                    vence_todos = False
                                    break
                            if vence_todos:
                                classificacao_final[candidato] = 1
                                #retira das listas de habilitados o candidato classificado
                                for chave, valores in dicionario_ordenado.items():
                                    if candidato in valores:
                                        valores.remove(candidato)
                                break                            
                        
                #se nenhuma prova desempatou, vai para a escolha do usuário. Aqui viria esse código
                #if len(classificacao_final) == posicao:
                    #colocar aqui a escolha do usuário
                    
                '''

        for lugar, (candidato, indicacoes) in enumerate(classificacao_final.items(), start=1):
            print(
                f"{candidato} foi habilitado(a), em {lugar}º lugar, com {indicacoes} indicações.")


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
            print(row.candidato, row.media)
            if float(row.media) >= float(7):
                # print("maior")
                num_medias[row.candidato] += 1
            else:
                if row.candidato not in num_medias:
                    num_medias[row.candidato] = 0
        print("num_medias: ", num_medias)

        # Atualize os candidatos correspondentes na base de dados
        for candidato, count in num_medias.items():
            # print(count)
            if count >= 3:
                Candidato.objects.filter(
                    nome=candidato).update(habilitado=True)
                print(f'{candidato}: {count} --> Aprovado')
            else:
                Candidato.objects.filter(
                    nome=candidato).update(habilitado=False)
                print(f'{candidato}: {count} --> Reprovado')

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
