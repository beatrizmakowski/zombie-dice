'''
Implementação em Python do jogo Zombie Dice.
Aluna: Beatriz Makowski
Arquivo criado em 07/08/2022
Última alteração: 22/08/2022.
'''

import os
from pickle import FALSE
import random
from re import I
import time

# Global variables
NUMBER_OF_PĹAYERS = 0
CURRENT_PLAYER = 0
PLAYERS = []
WINNER = None
ALL_DICE = ['CPCTPC', 'CPCTPC', 'CPCTPC', 'CPCTPC', 'CPCTPC', 'CPCTPC', # 6 dados verdes 
            'TPCTPC', 'TPCTPC', 'TPCTPC','TPCTPC',                      # 4 dados amarelos
            'TPTCPT', 'TPTCPT', 'TPTCPT']                               # 3 dados vermelhos
AVAILABLE_DICE = ALL_DICE   # Var. global sem os dados que já foram sorteados na jogada atual

class format:
    # Fonte: https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    BOLD = '\033[1m'
    HEADER = '\033[95m'
    NORMAL = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_FORMATTING = '\033[0m'

class Player:
    def __init__(self, number, name) -> None:
        self.number = number
        self.name = name
        self.score = 0
        self.brains = 0
        self.shots = 0
        self.footprints = 0

# Custom functions
clear = lambda: os.system('clear')


def customPrint(text, type=format.NORMAL, bold=False):
    font_weight = format.BOLD if bold == True else ''
    print(f'{font_weight}{type}{text}{format.END_FORMATTING}')


def get_number_of_players():
    global NUMBER_OF_PĹAYERS
    while True:
        try:
            NUMBER_OF_PĹAYERS = int(input(f'{format.NORMAL}\nQuantas pessoas irão jogar? {format.END_FORMATTING}'))
        except ValueError:
            customPrint('Não entendi... (╥_╥) Por favor, digite apenas números inteiros.', type=format.WARNING)
        else: 
            if NUMBER_OF_PĹAYERS >= 2:
                break
            customPrint('O número mínimo de jogadores é 2!', type=format.WARNING)


def get_players_names():
    for i in range(NUMBER_OF_PĹAYERS):
        try:
            name = input(f'{format.BOLD}{format.NORMAL}Digite o nome do jogador {i + 1}: {format.END_FORMATTING}')
        except:
            customPrint('Não entendi... (╥_╥) Por favor, digite novamente.', type=format.WARNING)
        else:
            newPlayer = Player(i + 1, name)
            PLAYERS.append(newPlayer)


def draw_dice(number_of_draws):
    global AVAILABLE_DICE
    dice = []
    number_of_green_dice = number_of_yellow_dice = number_of_red_dice = 0
    plural_green_dice = plural_yellow_dice = plural_red_dice = ''

    customPrint('Sorteando dados...', )

    for i in range(number_of_draws):
        die = random.choice(AVAILABLE_DICE)
        dice.append(die)
        if die == 'CPCTPC':
            number_of_green_dice += 1
        elif die == 'TPCTPC':
            number_of_yellow_dice += 1
        elif die == 'TPTCPT':
            number_of_red_dice += 1

    if number_of_green_dice > 1:
        plural_green_dice = 's'
    elif number_of_green_dice == 0:
        number_of_green_dice = 'nenhum'

    if number_of_yellow_dice > 1:
        plural_yellow_dice = 's'
    elif number_of_yellow_dice == 0:
        number_of_yellow_dice = 'nenhum'

    if number_of_red_dice > 1:
        plural_red_dice = 's'
    elif number_of_red_dice == 0:
        number_of_red_dice = 'nenhum'

    customPrint(f'Foram sorteados {number_of_green_dice} dado{plural_green_dice} verde{plural_green_dice}, '
                f'{number_of_yellow_dice} dado{plural_yellow_dice} amarelo{plural_yellow_dice} e '
                f'{number_of_red_dice} dado{plural_red_dice} vermelho{plural_red_dice}.')
    
    roll_dice(dice)


def roll_dice(dice):
    global AVAILABLE_DICE
    global PLAYERS
    colors = []
    results = []

    customPrint('Rolando dados...', )

    for die in dice:

        if die == 'CPCTPC':
            colors.append(format.NORMAL)
        elif die == 'TPCTPC':
            colors.append(format.WARNING)
        else:
            colors.append(format.FAIL)

        result = random.choice(die)
        results.append(result)

        if result == 'P':
            PLAYERS[CURRENT_PLAYER].footprints += 1
            AVAILABLE_DICE.append(die) # Os dados [P] podem ser sorteados novamente se o jogador quiser continuar
        elif result == 'C':
            PLAYERS[CURRENT_PLAYER].brains += 1
        elif result == 'T':
            PLAYERS[CURRENT_PLAYER].shots += 1
    
    print_rolled_dice(colors, results)


def print_rolled_dice(colors, results):
    for i in range(len(results)):
        print(f'{colors[i]} ———  {format.END_FORMATTING}', end='')
    print('\n', end='')
    for i in range(len(results)):
        print(f'{colors[i]}| {results[i]} | {format.END_FORMATTING}', end='')
    print('\n', end='')
    for i in range(len(results)):
        print(f'{colors[i]} ———  {format.END_FORMATTING}', end='')
    print('\n', end='')


def confirm_if_player_will_continue():
    while True:
        answer = input(f'{format.BOLD}{format.NORMAL}\n'
                       f'Você deseja continuar a rodada? Digite "S" ou "N": '
                       f'{format.END_FORMATTING}').upper()
        if answer == 'S':
            return True
        elif answer == 'N':
            return False
        else:
            customPrint('Hum, não entendi... (╥_╥) Por favor, digite novamente.', type=format.WARNING)


def print_scoreboard():
    global WINNER
    customPrint(f'\nScoreboard:', bold=True)
    for j in range(NUMBER_OF_PĹAYERS):
        customPrint(f'{PLAYERS[j].name}: {PLAYERS[j].score}')
        if PLAYERS[j].score >= 13:
            WINNER = PLAYERS[j]
    if WINNER:
        end_the_game()


def end_the_game():
    customPrint(f'\nWow! {WINNER.name} ganhou o jogo com {WINNER.score} pontos! \(•◡•)/', type=format.HEADER, bold=True)
    input(f'{format.HEADER}Pressione qualquer tecla para encerrar o jogo.\n{format.END_FORMATTING}')
    quit()


# Main
clear()
customPrint('** Bem vindo(a) ao jogo Zombie Dice! \(•◡•)/ **', type=format.HEADER, bold=True)
customPrint('Pressione Ctrl+Z a qualquer momento para sair do jogo.', type=format.HEADER)

get_number_of_players()
get_players_names()

customPrint('Começando uma nova partida! \(•◡•)/', type=format.HEADER, bold=True)
winner = False

while True:
    for i in range(NUMBER_OF_PĹAYERS):
        CURRENT_PLAYER = i
        player_will_continue = True

        print_scoreboard()
        
        customPrint(f'\n{PLAYERS[i].name}, é a sua vez!\n', bold=True)
        input(f'{format.NORMAL}Pressione qualquer tecla para continuar.\n{format.END_FORMATTING}')
        number_of_dice_to_draw = 3
        clear()

        while player_will_continue:
            plural_points = plural_shots = ''

            draw_dice(number_of_dice_to_draw)

            customPrint(f'\nSeu score atual é:')
            customPrint(f'{"Cérebros":^10}|{"Pegadas":^10}|{"Tiros":^10}')
            customPrint(f'{PLAYERS[i].brains:^10}|{PLAYERS[i].footprints:^10}|{PLAYERS[i].shots:^10}')

            if PLAYERS[i].shots >= 3:
                customPrint(f'\nAh não! Você levou {PLAYERS[i].shots} tiros e perdeu todos os pontos acumulados nesta '
                            f'rodada! (╥_╥)', bold=True, type=format.FAIL)
                PLAYERS[i].brains = 0
                player_will_continue = False
                continue
            
            if PLAYERS[i].brains > 1:
                plural_points = 's'
            if 3 - PLAYERS[i].shots > 1:
                plural_shots = 's'

            customPrint(f'\nVocê pode encerrar esta rodada e ganhar {PLAYERS[i].brains} ponto{plural_points} ou sortear '
                        f'mais 3 dados e tentar aumentar seu score!')
            customPrint(f'Porém, se você levar mais {3 - PLAYERS[i].shots} tiro{plural_shots}, sua vez acabará e você '
                        f'perderá todos os pontos que acumulou até agora...')
            
            number_of_dice_to_draw = 3 - PLAYERS[i].footprints
            PLAYERS[i].footprints = 0

            player_will_continue = confirm_if_player_will_continue()
            clear()
        
        PLAYERS[i].score += PLAYERS[i].brains
        PLAYERS[i].brains = 0
        PLAYERS[i].footprints = 0
        PLAYERS[i].shots = 0
