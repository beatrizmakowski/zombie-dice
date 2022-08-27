'''
Implementação em Python do jogo Zombie Dice.
Aluna: Beatriz Makowski (RA 1112022201591)
Curso: Superior de Tecnologia em Análise de Desenvolvimento de Sistemas
Arquivo criado em: 07/08/2022
Última alteração: 27/08/2022
'''

import os
import random


# <--- Variáveis globais --->

NUMERO_DE_JOGADORES = 0
JOGADOR_ATUAL = 0
VENCEDOR = None

''' Lista para armazenar os jogadores '''
JOGADORES = []

'''  Lista para representar o tubo onde onde serão colocados os treze dados inicialmente '''
TODOS_OS_DADOS = ['CPCTPC', 'CPCTPC', 'CPCTPC', 'CPCTPC', 'CPCTPC', 'CPCTPC', # 6 dados verdes 
                  'TPCTPC', 'TPCTPC', 'TPCTPC','TPCTPC', # 4 dados amarelos
                  'TPTCPT', 'TPTCPT', 'TPTCPT'] # 3 dados vermelhos
                

'''  Lista que será manipulada para desconsiderar os dados já sorteados na jogada atual '''
DADOS_DISPONIVEIS = TODOS_OS_DADOS


# <--- Classes personalizadas --->

class Format:
    '''
    Classe criada para facilitar a Formatação do texto no terminal.
    Fonte: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    '''
    NEGRITO = '\033[1m'
    ROSA = '\033[95m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    END = '\033[0m'


class Jogador:
    ''' Classe criada para facilitar o controle das informações dos jogadores '''

    def __init__(self, numero, nome) -> None:
        self.numero = numero
        self.nome = nome
        self.pontos = 0
        self.cerebros = 0
        self.tiros = 0
        self.pegadas = 0

    def resetar_cerebros_tiros_pegadas(self):
        self.cerebros = 0
        self.tiros = 0
        self.pegadas = 0


# <--- Funções personalizadas --->

''' Limpa a tela do terminal '''
clear = lambda: os.system('cls')


def customPrint(text, type='', NEGRITO=False):
    ''' Função que facilita a customização do texto impresso no terminal '''

    font_weight = Format.NEGRITO if NEGRITO == True else ''
    print(f'{font_weight}{type}{text}{Format.END}')


def obter_numero_de_jogadores():
    ''' Pergunta ao usuário o número de jogadores, repetindo até que o input seja um número maior ou igual a 2 '''

    global NUMERO_DE_JOGADORES
    while True:
        try:
            NUMERO_DE_JOGADORES = int(input(f'{Format.NEGRITO}{Format.ROSA}\n'
                                            f'Quantas pessoas irão jogar? '
                                            f'{Format.END}'))
        except ValueError:
            customPrint('Não entendi... (╥_╥) Por favor, digite apenas números inteiros.',
                        type=Format.AMARELO)
        else: 
            if NUMERO_DE_JOGADORES >= 2:
                break
            customPrint('O número mínimo de jogadores é 2!', type=Format.AMARELO)


def obter_nomes_dos_jogadores():
    ''' Pergunta ao usuário o número de jogadores, repetindo até que o input seja uma string válida '''

    for i in range(NUMERO_DE_JOGADORES):
        while True:
            try:
                nome = input(f'{Format.NEGRITO}{Format.ROSA}'
                             f'Digite o nome do jogador {i + 1}: '
                             f'{Format.END}').title()
            except:
                customPrint('Não entendi... (╥_╥) Por favor, digite novamente.', type=Format.AMARELO)
            else:
                novoJogador = Jogador(i + 1, nome)
                JOGADORES.append(novoJogador)
                break


def sortear_dados(numero_de_sorteios):
    ''' Usa a biblioteca random para sortear dados dentre as opções disponíveis na variável global DADOS_DISPONIVEIS
    Imprime no terminal quantos dados de cada cor foram sorteados.
    '''
    
    global DADOS_DISPONIVEIS
    dados = []
    numero_de_dados_verdes = numero_de_dados_amarelos = numero_de_dados_vermelhos = 0
    plural_dados_verdes = plural_dados_amarelos = plural_dados_vermelhos = ''

    customPrint('\nSorteando dados...')

    for _ in range(numero_de_sorteios):

        dado = random.choice(DADOS_DISPONIVEIS)
        dados.append(dado)

        if dado == 'CPCTPC':
            numero_de_dados_verdes += 1
        elif dado == 'TPCTPC':
            numero_de_dados_amarelos += 1
        elif dado == 'TPTCPT':
            numero_de_dados_vermelhos += 1

    if numero_de_dados_verdes > 1:
        plural_dados_verdes = 's'
    elif numero_de_dados_verdes == 0:
        numero_de_dados_verdes = 'nenhum'

    if numero_de_dados_amarelos > 1:
        plural_dados_amarelos = 's'
    elif numero_de_dados_amarelos == 0:
        numero_de_dados_amarelos = 'nenhum'

    if numero_de_dados_vermelhos > 1:
        plural_dados_vermelhos = 's'
    elif numero_de_dados_vermelhos == 0:
        numero_de_dados_vermelhos = 'nenhum'

    customPrint(f'\nForam sorteados {Format.NEGRITO}{Format.VERDE}{numero_de_dados_verdes} dado{plural_dados_verdes} verde{plural_dados_verdes}{Format.END}, '
                f'{Format.NEGRITO}{Format.AMARELO}{numero_de_dados_amarelos} dado{plural_dados_amarelos} amarelo{plural_dados_amarelos}{Format.END} e '
                f'{Format.NEGRITO}{Format.VERMELHO}{numero_de_dados_vermelhos} dado{plural_dados_vermelhos} vermelho{plural_dados_vermelhos}{Format.END}.')
    
    input(f'{Format.ROSA}\n[Pressione qualquer tecla para rolar os dados]{Format.END}')

    jogar_dados(dados)


def jogar_dados(dados):
    ''' Usa a biblioteca random para sortear uma face de cada dado sorteado pela função sortear_dados()
    Atualiza as informações do jogador atual
    '''
    global DADOS_DISPONIVEIS
    global JOGADORES
    cores = []
    resultados = []

    clear()
    customPrint('\nRolando os dados...\n')

    for dado in dados:

        if dado == 'CPCTPC': # Dado verde
            cores.append(Format.VERDE)
        elif dado == 'TPCTPC': # Dado amarelo
            cores.append(Format.AMARELO)
        else: # Dado vermelho
            cores.append(Format.VERMELHO)

        resultado = random.choice(dado)
        resultados.append(resultado)

        if resultado == 'P': # [P] = pegadas
            JOGADORES[JOGADOR_ATUAL].pegadas += 1
            DADOS_DISPONIVEIS.append(dado) # Os dados [P] podem ser sorteados novamente se o jogador quiser continuar
        elif resultado == 'C': # [C] = cérebros
            JOGADORES[JOGADOR_ATUAL].cerebros += 1
        elif resultado == 'T': # [T] = tiros
            JOGADORES[JOGADOR_ATUAL].tiros += 1
    
    imprimir_dados_jogados(cores, resultados)


def imprimir_dados_jogados(cores, resultados):
    ''' Imprime no terminal as faces sorteadas de cada dado, com as cores correspondentes '''

    for i in range(len(resultados)):
        print(f'{Format.NEGRITO}{cores[i]} ———  {Format.END}', end='')
    print('\n', end='')

    for i in range(len(resultados)):
        print(f'{Format.NEGRITO}{cores[i]}| {resultados[i]} | {Format.END}', end='')
    print('\n', end='')

    for i in range(len(resultados)):
        print(f'{Format.NEGRITO}{cores[i]} ———  {Format.END}', end='')
    print('\n', end='')


def confirmar_se_jogador_quer_continuar():
    ''' Pergunta ao jogador se ele quer continuar a jogar ou encerrar a rodada, 
    repetindo até que o input seja uma string válida.
    '''

    while True:
        resposta = input(f'{Format.NEGRITO}{Format.ROSA}\n'
                       f'Você deseja continuar a rodada? Digite "S" ou "N": '
                       f'{Format.END}').upper()
        if resposta == 'S':
            return True
        elif resposta == 'N':
            return False
        else:
            customPrint('Hum, não entendi... (╥_╥) Por favor, digite novamente.', type=Format.AMARELO)


def imprimir_placar():
    ''' Imprime no terminal o placar de pontos atual.
    Verifica se há um vencedor (jogador com 13 pontos ou mais)
    Caso sim, chama a função de encerrar o jogo.
    '''
    
    global VENCEDOR
    customPrint('\nPlacar:')

    for j in range(NUMERO_DE_JOGADORES):
        customPrint(f'{JOGADORES[j].nome}: {JOGADORES[j].pontos}')

        if JOGADORES[j].pontos >= 13:
            VENCEDOR = JOGADORES[j]

    if VENCEDOR:
        encerrar_o_jogo()


def encerrar_o_jogo():
    ''' Imprime a mensagem de encerramento e encerra a execução do programa '''

    customPrint(f'\nUau! {VENCEDOR.nome} ganhou o jogo com {VENCEDOR.pontos} pontos! \(•◡•)/', type=Format.ROSA, NEGRITO=True)
    input(f'{Format.ROSA}\n[Pressione qualquer tecla para encerrar o jogo]\n{Format.END}')
    quit()


# <--- Main --->

clear()
customPrint('** Bem vindo(a) ao jogo Zombie dados! \(•◡•)/ **', type=Format.ROSA, NEGRITO=True)
customPrint('[Pressione Ctrl+Z a qualquer momento para sair do jogo]', type=Format.ROSA)

obter_numero_de_jogadores()
obter_nomes_dos_jogadores()

clear()
customPrint('\nComeçando uma nova partida! \(•◡•)/', type=Format.ROSA, NEGRITO=True)

while True:
    for i in range(NUMERO_DE_JOGADORES):
        JOGADOR_ATUAL = i
        jogador_quer_continuar = True

        imprimir_placar()
        
        customPrint(f'\n{JOGADORES[i].nome}, é a sua vez!\n', NEGRITO=True, type=Format.ROSA)
        DADOS_DISPONIVEIS = TODOS_OS_DADOS
        input(f'{Format.ROSA}[Pressione qualquer tecla sortear os dados]\n{Format.END}')
        numero_de_dados_para_sortear = 3
        clear()

        while jogador_quer_continuar:
            plural_pontos = plural_tiros = ''

            sortear_dados(numero_de_dados_para_sortear)

            customPrint(f'\nSua pontuação atual é: \n')
            customPrint(f'{"Cérebros":^10}|{"Pegadas":^10}|{"Tiros":^10}')
            customPrint(f'{JOGADORES[i].cerebros:^10}|{JOGADORES[i].pegadas:^10}|{JOGADORES[i].tiros:^10}')

            if JOGADORES[i].tiros >= 3:
                customPrint(f'\nAh não! Você levou {JOGADORES[i].tiros} tiros e perdeu todos os pontos acumulados nesta '
                            f'rodada! (╥_╥)', NEGRITO=True, type=Format.VERMELHO)           
                JOGADORES[i].cerebros = 0
                jogador_quer_continuar = False
                input(f'{Format.ROSA}\n[Pressione qualquer tecla para continuar]\n{Format.END}')
                clear()
                continue
            
            if JOGADORES[i].cerebros > 1:
                plural_pontos = 's'
            if 3 - JOGADORES[i].tiros > 1:
                plural_tiros = 's'

            customPrint(f'\nVocê pode encerrar esta rodada e ganhar '
                        f'{Format.NEGRITO}{Format.VERDE}{JOGADORES[i].cerebros} ponto{plural_pontos}{Format.END} '
                        f'ou jogar novamente e tentar aumentar seu pontos!')
            customPrint(f'Porém, se você levar mais '
                        f'{Format.NEGRITO}{Format.VERMELHO}{3 - JOGADORES[i].tiros} tiro{plural_tiros}{Format.END}, '
                        f'sua vez acabará e você perderá todos os pontos que acumulou até agora...')

            jogador_quer_continuar = confirmar_se_jogador_quer_continuar()
            clear()
        
        JOGADORES[i].pontos += JOGADORES[i].cerebros
        JOGADORES[i].resetar_cerebros_tiros_pegadas()
