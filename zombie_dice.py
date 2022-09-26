'''
Implementação em Python do jogo Zombie Dice
Aluna: Beatriz Makowski (RA 1112022201591)
Curso: Superior de Tecnologia em Análise de Desenvolvimento de Sistemas
Arquivo criado em: 07/08/2022
Última alteração: 26/09/2022

Readme disponível em: https://github.com/beatrizmakowski/zombie-dice#readme
'''

import os
import random


# <--- Variáveis globais --->

numero_de_jogadores = 0
jogador_atual = 0
vencedor = None
jogador = [] # Lista para armazenar os jogadores
dado_verde = ('C', 'P', 'C', 'T', 'P', 'C')
dado_amarelo = ('T', 'P', 'C', 'T', 'P', 'C')
dado_vermelho = ('T', 'P', 'T', 'C', 'P', 'T')
numero_de_dados_para_sortear = 3

def inicializar_copo_dados():
    ''' Inicializa o copo de dados com 6 dados verdes, 4 dados amarelos e 3 dados vermelhos '''
    global copo_dados

    copo_dados = []
    
    for _ in range(6):
        copo_dados.append(dado_verde)
    for _ in range(4):
        copo_dados.append(dado_amarelo)
    for _ in range(3):
        copo_dados.append(dado_vermelho)


copo_dados = [] # Lista para representar o copo onde onde serão colocados os treze dados inicialmente
inicializar_copo_dados()       
dados_disponiveis = copo_dados # Lista que será manipulada para desconsiderar os dados já sorteados na jogada atual


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
    ''' Classe criada para facilitar o controle das informações dos jogador '''

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


class CopoVazio(Exception):
    '''Exceção customizada que é 'raised' quando a quantidade de dados no copo é zero'''
    customPrint(f'\nO copo está vazio!', NEGRITO=True, type=Format.VERMELHO) 


def obter_numero_de_jogadores():
    ''' Pergunta ao usuário o número de jogador, repetindo até que o input seja um número maior ou igual a 2 '''

    global numero_de_jogadores
    while True:
        try:
            numero_de_jogadores = int(input(f'{Format.NEGRITO}{Format.ROSA}\n'
                                            f'Quantas pessoas irão jogar? '
                                            f'{Format.END}'))
        except ValueError:
            customPrint('Não entendi... (╥_╥) Por favor, digite apenas números inteiros.',
                        type=Format.AMARELO)
        else: 
            if numero_de_jogadores >= 2:
                break
            customPrint('O número mínimo de jogador é 2!', type=Format.AMARELO)


def obter_nomes_dos_jogadores():
    ''' Pergunta ao usuário o número de jogador, repetindo até que o input seja uma string válida '''

    for i in range(numero_de_jogadores):
        while True:
            try:
                nome = input(f'{Format.NEGRITO}{Format.ROSA}'
                             f'Digite o nome do jogador {i + 1}: '
                             f'{Format.END}').title()
            except:
                customPrint('Não entendi... (╥_╥) Por favor, digite novamente.', type=Format.AMARELO)
            else:
                novoJogador = Jogador(i + 1, nome)
                jogador.append(novoJogador)
                break


def imprimir_dados_disponiveis_no_copo():
    ''' Imprime na saída do console quais os dados que estão armazenados no copo em cada uma das jogadas (Checklist Semana 5) '''

    numero_de_dados_verdes = numero_de_dados_amarelos = numero_de_dados_vermelhos = 0
    plural_dados_verdes = plural_dados_amarelos = plural_dados_vermelhos = ''

    for dado in copo_dados:
        if dado == dado_verde:
            numero_de_dados_verdes += 1
        elif dado == dado_amarelo:
            numero_de_dados_amarelos += 1
        elif dado == dado_vermelho:
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

    customPrint(f'\nDados disponíveis no copo: {Format.NEGRITO}{Format.VERDE}{numero_de_dados_verdes} dado{plural_dados_verdes} verde{plural_dados_verdes}{Format.END}, '
                f'{Format.NEGRITO}{Format.AMARELO}{numero_de_dados_amarelos} dado{plural_dados_amarelos} amarelo{plural_dados_amarelos}{Format.END} e '
                f'{Format.NEGRITO}{Format.VERMELHO}{numero_de_dados_vermelhos} dado{plural_dados_vermelhos} vermelho{plural_dados_vermelhos}{Format.END}.')


def sortear_dados(numero_de_sorteios):
    ''' Usa a biblioteca random para sortear dados dentre as opções disponíveis na variável global copo_dados
    Imprime no terminal quantos dados de cada cor foram sorteados.
    '''

    global copo_dados

    if len(copo_dados) == 0:
        raise CopoVazio
    elif len(copo_dados) < 3:
        numero_de_sorteios = len(copo_dados)

    dados = []
    numero_de_dados_verdes = numero_de_dados_amarelos = numero_de_dados_vermelhos = 0
    plural_dados_verdes = plural_dados_amarelos = plural_dados_vermelhos = ''

    imprimir_dados_disponiveis_no_copo()
    customPrint('\nSorteando dados...')

    for _ in range(numero_de_sorteios):

        dado = random.choice(copo_dados) # Escolhe um dado do copo
        copo_dados.pop(copo_dados.index(dado)) # Remove o dado escolhido do copo
        dados.append(dado) # Adiciona o dado escolhido na lista de dados que serão rolados para sortear uma face

        if dado == dado_verde:
            numero_de_dados_verdes += 1
        elif dado == dado_amarelo:
            numero_de_dados_amarelos += 1
        elif dado == dado_vermelho:
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
    global dados_disponiveis
    global jogador
    cores = []
    resultados = []

    clear()
    customPrint('\nRolando os dados...\n')

    for dado in dados:

        if dado == dado_verde:
            cores.append(Format.VERDE)
        elif dado == dado_amarelo:
            cores.append(Format.AMARELO)
        else:
            cores.append(Format.VERMELHO)

        resultado = random.choice(dado)
        resultados.append(resultado)

        # 'P' == pegada
        # 'C' == cérebro
        # 'T' == tiro
        if resultado == 'P': 
            jogador[jogador_atual].pegadas += 1
            dados_disponiveis.append(dado) # Os dados que caírem na face 'P' podem ser sorteados na próxima jogada, se o jogador quiser continuar
        elif resultado == 'C': 
            jogador[jogador_atual].cerebros += 1
        elif resultado == 'T': 
            jogador[jogador_atual].tiros += 1
    
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


def confirmar_se_jogador_atual_quer_continuar():
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


def imprimir_pontuacao_do_jogador_atual(i):
    customPrint(f'\nSua pontuação atual é: \n')
    customPrint(f'{"Cérebros":^10}|{"Pegadas":^10}|{"Tiros":^10}')
    customPrint(f'{jogador[i].cerebros:^10}|{jogador[i].pegadas:^10}|{jogador[i].tiros:^10}')


def imprimir_placar():
    ''' Imprime no terminal o placar de pontos atual.
    Verifica se há um vencedor (jogador com 13 pontos ou mais)
    Caso sim, chama a função de encerrar o jogo.
    '''

    global vencedor

    titulo = '*** Placar ***'
    customPrint(f'\n{titulo:^20}', NEGRITO=True, type=Format.ROSA)
    customPrint(f'{"Jogador":^10}|{"Pontos":^10}', NEGRITO=True)
    customPrint('-'*21)

    for j in range(numero_de_jogadores):
        customPrint(f'{jogador[j].nome:^10}| {jogador[j].pontos:^10}')

        if jogador[j].pontos >= 13:
            vencedor = jogador[j]

    if vencedor:
        encerrar_o_jogo()


def encerrar_o_jogo():
    ''' Imprime a mensagem de encerramento e encerra a execução do programa '''

    customPrint(f'\nUau! {vencedor.nome} ganhou o jogo com {vencedor.pontos} pontos! Parabéns! \(•◡•)/', type=Format.ROSA, NEGRITO=True)
    input(f'{Format.ROSA}\n\n[Pressione qualquer tecla para encerrar o jogo]\n{Format.END}')
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

    for i in range(numero_de_jogadores):

        jogador_atual = i
        jogador_atual_quer_continuar = True

        imprimir_placar()
        
        customPrint(f'\n{jogador[i].nome}, é a sua vez!\n', NEGRITO=True, type=Format.ROSA)
        input(f'{Format.ROSA}[Pressione qualquer tecla sortear os dados]\n{Format.END}')
        clear()

        while jogador_atual_quer_continuar:

            plural_pontos = plural_tiros = ''

            try:
                sortear_dados(numero_de_dados_para_sortear)
            except CopoVazio:
                input(f'{Format.ROSA}\nPassando a vez para o próximo jogador...\n{Format.END}')
                jogador_atual_quer_continuar = False
                continue

            imprimir_pontuacao_do_jogador_atual(i)

            if jogador[i].tiros >= 3:
                customPrint(f'\nAh não! Você levou {jogador[i].tiros} tiros e perdeu todos os pontos acumulados nesta '
                            f'rodada! (╥_╥)', NEGRITO=True, type=Format.VERMELHO)           
                jogador[i].cerebros = 0
                jogador_atual_quer_continuar = False
                input(f'{Format.ROSA}\n[Pressione qualquer tecla para continuar]\n{Format.END}')
                clear()
                continue
            
            if jogador[i].cerebros > 1:
                plural_pontos = 's'
            if 3 - jogador[i].tiros > 1:
                plural_tiros = 's'

            customPrint(f'\nVocê pode encerrar esta rodada e ganhar '
                        f'{Format.NEGRITO}{Format.VERDE}{jogador[i].cerebros} ponto{plural_pontos}{Format.END} '
                        f'ou jogar novamente e tentar aumentar sua pontuação!')
            customPrint(f'Porém, se você levar mais '
                        f'{Format.NEGRITO}{Format.VERMELHO}{3 - jogador[i].tiros} tiro{plural_tiros}{Format.END}, '
                        f'sua vez acabará e você perderá todos os pontos que acumulou até agora...')

            jogador_atual_quer_continuar = confirmar_se_jogador_atual_quer_continuar()
            clear()
        
        inicializar_copo_dados()
        dados_disponiveis = copo_dados

        jogador[i].pontos += jogador[i].cerebros
        jogador[i].resetar_cerebros_tiros_pegadas()
