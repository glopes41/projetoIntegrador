
def calcula_classificacao_final():

    # Para rodar o código, coloque como comentário as aspas triplas de abertura e fechamento dos testes abaixo


    """
                        #TESTE 1

    # substituir o valor da lista por um código genérico que gere uma lista dos candidatos habilitados
    candidatos_habilitados = ['Ana',
                            'Cléber',
                            'Caio',
                            'Marcelo'
                            ] 

# substituir o valor destes dicts por um código genérico que os gere a partir dos dados do concurso
dicionario_ordenado = {
    'Examinador 1': ['Ana', 'Marcelo', 'Caio', 'Cléber'],
    'Examinador 2': ['Cléber', 'Marcelo', 'Caio', 'Ana'],
    'Examinador 3': ['Caio', 'Ana', 'Marcelo', 'Cléber'],
    'Examinador 4': ['Marcelo', 'Caio', 'Ana', 'Cléber'],
    'Examinador 5': ['Ana', 'Marcelo', 'Caio', 'Cléber']
}
"""


    """
                        #TESTE 2

    # substituir o valor da lista por um código genérico que gere uma lista dos candidatos habilitados
    candidatos_habilitados = ['Ana',
                            'Marcelo',
                            'Caio',
                            'Cléber'
                            ] 

# substituir o valor destes dicts por um código genérico que os gere a partir dos dados do concurso
dicionario_ordenado = {
    'Examinador 1': ['Ana', 'Marcelo', 'Caio', 'Cléber'],
    'Examinador 2': ['Cléber', 'Marcelo', 'Caio', 'Ana'],
    'Examinador 3': ['Ana', 'Caio', 'Marcelo', 'Cléber'],
    'Examinador 4': ['Marcelo', 'Caio', 'Ana', 'Cléber'],
    'Examinador 5': ['Ana', 'Marcelo', 'Caio', 'Cléber']
}
"""


    """
                        #TESTE 3 - TROCAR num_habilitados PARA 5

    # substituir o valor da lista por um código genérico que gere uma lista dos candidatos habilitados
    candidatos_habilitados = ['Ana',
                            'Cléber',
                            'Caio',
                            'Mateus',
                            'Marcelo'
                            ] 

    # substituir o valor destes dicts por um código genérico que os gere a partir dos dados do concurso
    dicionario_ordenado = {
        'Examinador 1': ['Ana', 'Marcelo', 'Caio', 'Cléber','Mateus'],
        'Examinador 2': ['Cléber', 'Marcelo', 'Caio', 'Ana','Mateus'],
        'Examinador 3': ['Caio', 'Ana', 'Marcelo', 'Cléber','Mateus'],
        'Examinador 4': ['Marcelo', 'Caio', 'Ana', 'Cléber','Mateus'],
        'Examinador 5': ['Mateus','Ana', 'Marcelo', 'Caio', 'Cléber']
    }
    """


acumulador = 0
# substituir o "4" por uma consulta genérico ao número de habilitados
num_habilitados = 4
empate_com_duas_indicacoes = []
classificacao_final = {}

    for posicao in range(num_habilitados):
        for candidato in candidatos_habilitados:

        for chave, valores in dicionario_ordenado.items():
            if valores:
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
            for chave, valores in dicionario_ordenado.items():
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
        for chave, valores in dicionario_ordenado.items():
            if empate_com_duas_indicacoes[0] in valores:
                valores.remove(empate_com_duas_indicacoes[0])

    # verifica se houve empate de indicações
    if len(empate_com_duas_indicacoes) == 2:

        # CÓDIGO PROVISÓRIO!!!!

        # coloca o primeiro que teve 2 indicações como o próximo na classificação
        classificacao_final[empate_com_duas_indicacoes[0]] = 2
        # retira das listas de habilitados o candidato classificado
        for chave, valores in dicionario_ordenado.items():
            if empate_com_duas_indicacoes[0] in valores:
                valores.remove(empate_com_duas_indicacoes[0])
        # zera a lista de empate
        empate_com_duas_indicacoes = []

        # DEPOIS SERÁ PRECISO COLOCAR:
    # colocar o desempate pela média da prova didática
    # se continuar empatado, colocar o desempate pela média da prova de títulos
    # se continuar empatado, colocar o desempate por escolha do usuário. MAS ISSO NÃO É NECESSÁRIO INICIALMENTE. QUASE IMPOSSÍVEL ACONTECER.

    # verifica se todos os candidatos empataram com 1 indicação
    if len(classificacao_final) == posicao:
        # CÓDIGO PROVISÓRIO!!!!

        # coloca qualquer um na classificação
        for candidato in candidatos_habilitados:

            for chave, valores in dicionario_ordenado.items():
                if valores:
                    if candidato == valores[0]:
                        classificacao_final[candidato] = 1
                        break

            for chave, valores in dicionario_ordenado.items():
                if candidato in valores:
                    valores.remove(candidato)
            break

        # DEPOIS SERÁ PRECISO COLOCAR:
    # colocar o desempate pela média da prova didática
    # se continuar empatado, colocar o desempate pela média da prova de títulos
    # se continuar empatado, colocar o desempate por escolha do usuário. MAS ISSO NÃO É NECESSÁRIO INICIALMENTE. QUASE IMPOSSÍVEL ACONTECER.


print(classificacao_final)
print(dicionario_ordenado)
