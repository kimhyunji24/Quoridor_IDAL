import os
from random import sample
from time import sleep
from board import Board
from player import Player
from random_bot import Random_Bot

board = Board()
#players = [Random_Bot(board, "B1"), YJ(board)]
players = [Random_Bot(board, "B1"), Random_Bot(board, "B2")]
Games = 10
board.quoridors(Games, players, print_board=True)

# winning_score = 100
# while players[0].score<winning_score and players[1].score<winning_score:
#     first = sample(range(1,3),1)[0]
#     board.join(players, first)
#     while not board.is_finish(verbose=True):
#         os.system('cls')
#         board.one_play()
#         board.print_board_square()
#         print("Score  [{} : {}]".format(players[0].score, players[1].score))
#         #sleep(1)
#     board.initialize()
# os.system('cls')
print("[{}  {} : {}  {}]".format(players[0].name,players[0].score,players[1].score,players[1].name))
