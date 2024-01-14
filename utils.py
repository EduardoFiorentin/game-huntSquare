from random import randint
from config import *

def change_target_position():
    return [randint(50, WIDTH - MARGE_TARGET), randint(50, HEIGHT - MARGE_TARGET)]

def game_over(player):
    return player.bottom > HEIGHT or player.top < 0 or player.left < 0 or player.right > WIDTH