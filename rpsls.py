# codeskupltor : http://www.codeskulptor.org/
# I can't save.......zzz,and the version is python3

import random

def name_to_number(name):
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4
    else:
        print("NameInstructor is Wrong!")
        return -1

def number_to_name(number):
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'
    else:
        print("NumberInstructor is Wrong!")
        return 'Error'

def rpsls(player_choice):
    player_number = name_to_number(player_choice)
    comp_number = random.randrange(5)
    if (player_number - comp_number) % 4 < 2:
        print()
        print('Player chooses ', player_choice)
        print('Computer chooses ', number_to_name(comp_number))
        print('Player wins!')
    elif (player_number - comp_number) % 4 >= 2:
        print()
        print('Player chooses ', player_choice)
        print('Computer chooses ', number_to_name(comp_number))
        print('Computer wins!')
    else:
        print('Unkonwn Error!!')

rpsls('rock')
rpsls('Spock')
rpsls('paper')
rpsls('lizard')
rpsls('scissors')
