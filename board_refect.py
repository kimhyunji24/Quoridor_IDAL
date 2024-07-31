import os
import numpy as np
from random import sample
from time import sleep
from BFS import *

class Board:
    def __init__(self):
        self.rows = 9
        self.cols = 9
        self.hwalls = np.zeros((self.rows - 1, self.cols))
        self.vwalls = np.zeros((self.rows, self.cols - 1))
        self.points = np.zeros((self.rows - 1, self.cols - 1))
        self.symbol = ['♥', '♠']
        self.pawn = [[0, 4], [8, 4]]
        self.nplayer = len(self.pawn)
        self.turn = 0
        self.maze = np.zeros((self.rows * 2 + 1, self.cols * 2 + 1))
        self.maze[2::2, 2::2] = 1
        self.maze[0, :] = 1
        self.maze[self.rows * 2, :] = 1
        self.maze[:, 0] = 1
        self.maze[:, self.cols * 2] = 1
        self.num_walls = [10, 10]
        self.players = None

    def initialize(self):
        self.__init__()

    def quoridors(self, games, players, print_board=False):
        for i in range(games):
            first = sample(range(1, 3), 1)[0]
            self.join(players, first)
            while not self.is_finish():
                os.system('cls')
                self.one_play()
                if print_board: self.print_board()
                # sleep(1)
            self.initialize()

    def one_play(self):
        if self.players is not None:
            self.players[self.turn].play()
            self.turn = (self.turn + 1) % 2
        else:
            print("No players")

    def join(self, players, first):
        if first == 1:
            self.players = [players[0], players[1]]
            self.players[0].set_pawn(1)
            self.players[1].set_pawn(2)
        elif first == 2:
            self.players = [players[1], players[0]]
            self.players[0].set_pawn(1)
            self.players[1].set_pawn(2)

    def is_finish(self):
        if self.pawn[0][0] >= self.rows - 1:
            print(self.symbol[0] + " wins")
            self.players[0].score += 1
            return True
        if self.pawn[1][0] <= 0:
            print(self.symbol[1] + " wins")
            self.players[1].score += 1
            return True
        return False

    def print_board(self, mode='square'):
        board_s = (self.symbol[0] + ': {} ({} walls) \n' + self.symbol[1] + ': {} ({} walls)\n').format(
            self.players[0].name, self.num_walls[0], self.players[1].name, self.num_walls[1])
        for i in range(self.rows):
            for j in range(self.cols):
                if i == self.pawn[0][0] and j == self.pawn[0][1]:
                    board_s = board_s + self.symbol[0]
                elif i == self.pawn[1][0] and j == self.pawn[1][1]:
                    board_s = board_s + self.symbol[1]
                else:
                    board_s = board_s + '□'
                if j < self.cols - 1:
                    if self.vwalls[i, j] == 1:
                        board_s = board_s + '|'
                    else:
                        board_s = board_s + ' '
                else:
                    board_s = board_s + '\n'
            if i < self.rows - 1:
                for j in range(self.cols):
                    if self.hwalls[i, j] == 1:
                        board_s = board_s + '■'
                    else:
                        board_s = board_s + ' '
                    if j < self.cols - 1:
                        board_s = board_s + ' '
                board_s = board_s + '\n'
            if i == self.rows - 1:
                board_s = board_s + ('―' * (self.cols * 2 - 1)) + '\n'
        print(board_s)

    def move_player(self, direction, pawn):
        move_actions = {
            1: (1, 0), 2: (0, -1), 3: (-1, 0), 4: (0, 1),
            5: (2, 0), 6: (0, -2), 7: (-2, 0), 8: (0, 2),
            9: (1, 1), 10: (1, -1), 11: (-1, -1), 12: (-1, 1),
            13: (-1, -1), 14: (-1, 1), 15: (1, 1), 16: (1, -1)
        }
        if pawn > 0 and pawn <= self.nplayer and direction in move_actions:
            dx, dy = move_actions[direction]
            nx, ny = self.pawn[pawn - 1][0] + dx, self.pawn[pawn - 1][1] + dy
            if self.is_move_valid(pawn, direction, nx, ny):
                self.pawn[pawn - 1][0], self.pawn[pawn - 1][1] = nx, ny
                return True
        return False

    def is_move_valid(self, pawn, direction, nx, ny):
        if not (0 <= nx < self.rows and 0 <= ny < self.cols):
            return False
        wall_checks = {
            1: self.is_wall_down, 2: self.is_wall_left, 3: self.is_wall_up, 4: self.is_wall_right,
            5: self.is_wall_down_down, 6: self.is_wall_left_left, 7: self.is_wall_up_up, 8: self.is_wall_right_right,
            9: self.is_wall_down_right, 10: self.is_wall_down_left, 11: self.is_wall_left_down, 12: self.is_wall_left_up,
            13: self.is_wall_up_left, 14: self.is_wall_up_right, 15: self.is_wall_right_up, 16: self.is_wall_right_down
        }
        if direction in wall_checks and wall_checks[direction](pawn):
            return False
        return True

    def search_direction(self, pawn):
        directions = range(1, 17)
        return [d for d in directions if self.move_player(d, pawn)]

    def is_wall_down(self, pawn):
        if self.pawn[pawn-1][0] + 1 >= self.rows - 1:
            return False
        return self.hwalls[self.pawn[pawn-1][0], self.pawn[pawn-1][1]] == 1

    def is_wall_left(self, pawn):
        if self.pawn[pawn-1][1] - 1 < 0:
            return False
        return self.vwalls[self.pawn[pawn-1][0], self.pawn[pawn-1][1]-1] == 1

    def is_wall_up(self, pawn):
        if self.pawn[pawn-1][0] - 1 < 0:
            return False
        return self.hwalls[self.pawn[pawn-1][0]-1, self.pawn[pawn-1][1]] == 1

    def is_wall_right(self, pawn):
        if self.pawn[pawn-1][1] + 1 >= self.cols - 1:
            return False
        return self.vwalls[self.pawn[pawn-1][0], self.pawn[pawn-1][1]] == 1

    def is_wall_down_down(self, pawn):
        if self.pawn[pawn-1][0] + 2 >= self.rows:
            return False
        return self.hwalls[self.pawn[pawn-1][0] + 1, self.pawn[pawn-1][1]] == 1

    def is_wall_left_left(self, pawn):
        if self.pawn[pawn-1][1] - 2 < 0:
            return False
        return self.vwalls[self.pawn[pawn-1][0], self.pawn[pawn-1][1] - 2] == 1

    def is_wall_up_up(self, pawn):
        if self.pawn[pawn-1][0] - 2 < 0:
            return False
        return self.hwalls[self.pawn[pawn-1][0] - 2, self.pawn[pawn-1][1]] == 1

    def is_wall_right_right(self, pawn):
        if self.pawn[pawn-1][1] + 2 >= self.cols:
            return False
        return self.vwalls[self.pawn[pawn-1][0], self.pawn[pawn-1][1] + 1] == 1

    def is_wall_down_right(self, pawn):
        if self.pawn[pawn-1][0] + 1 >= self.rows or self.pawn[pawn-1][1] + 1 >= self.cols:
            return False
        return self.vwalls[self.pawn[pawn-1][0] + 1, self.pawn[pawn-1][1]] == 1

    def is_wall_down_left(self, pawn):
        if self.pawn[pawn-1][0] + 1 >= self.rows or self.pawn[pawn-1][1] - 1 < 0:
            return False
        return self.vwalls[self.pawn[pawn-1][0] + 1, self.pawn[pawn-1][1] - 1] == 1

    def is_wall_left_down(self, pawn):
        if self.pawn[pawn-1][0] + 1 >= self.rows or self.pawn[pawn-1][1] - 1 < 0:
            return False
        return self.hwalls[self.pawn[pawn-1][0], self.pawn[pawn-1][1] - 1] == 1

    def is_wall_left_up(self, pawn):
        if self.pawn[pawn-1][0] - 1 < 0 or self.pawn[pawn-1][1] - 1 < 0:
            return False
        return self.hwalls[self.pawn[pawn-1][0] - 1, self.pawn[pawn-1][1] - 1] == 1

    def is_wall_up_left(self, pawn):
        if self.pawn[pawn-1][0] - 1 < 0 or self.pawn[pawn-1][1] - 1 < 0:
            return False
        return self.vwalls[self.pawn[pawn-1][0] - 1, self.pawn[pawn-1][1] - 1] == 1

    def is_wall_up_right(self, pawn):
        if self.pawn[pawn-1][0] - 1 < 0 or self.pawn[pawn-1][1] + 1 >= self.cols:
            return False
        return self.vwalls[self.pawn[pawn-1][0] - 1, self.pawn[pawn-1][1]] == 1

    def is_wall_right_up(self, pawn):
        if self.pawn[pawn-1][0] - 1 < 0 or self.pawn[pawn-1][1] + 1 >= self.cols:
            return False
        return self.hwalls[self.pawn[pawn-1][0] - 1, self.pawn[pawn-1][1] + 1] == 1

    def is_wall_right_down(self, pawn):
        if self.pawn[pawn-1][0] + 1 >= self.rows or self.pawn[pawn-1][1] + 1 >= self.cols:
            return False
        return self.hwalls[self.pawn[pawn-1][0], self.pawn[pawn-1][1] + 1] == 1

    def put_wall(self, r, c, direction, pawn):
        if self.num_walls[pawn - 1] <= 0:
            print("{} has no walls.".format(self.players[pawn-1].name))
            return False
        if self.is_wall_valid(r, c, direction):
            self.num_walls[pawn-1] -= 1
            if direction == 1:
                self.hwalls[r, c:c + 2] = 1
            if direction == 2:
                self.vwalls[r:r + 2, c] = 1
            return True
        print("Invalid wall.")
        return False

    def is_wall_valid(self, r, c, direction):
        if r < 0 or r >= self.rows - 1 or c < 0 or c >= self.cols - 1:
            return False
        if direction == 1 and (self.hwalls[r, c] == 1 or self.hwalls[r, c + 1] == 1):
            return False
        if direction == 2 and (self.vwalls[r, c] == 1 or self.vwalls[r + 1, c] == 1):
            return False
        return not self.is_path_closed(r, c, direction)

    def is_path_closed(self, r, c, direction):
        player1_closed, player2_closed = True, True
        before_maze = self.maze.copy()
        if direction == 1:
            self.maze[r * 2 + 2, c * 2 + 1:c * 2 + 4] = 1
        if direction == 2:
            self.maze[r * 2 + 1:r * 2 + 4, c * 2 + 2] = 1

        for i in range(self.cols):
            if BFS(self.maze, (self.pawn[0][0] * 2 + 1, self.pawn[0][1] * 2 + 1), ((self.rows - 1) * 2 + 1, i * 2 + 1)) > 0:
                player1_closed = False
                break

        for i in range(self.cols):
            if BFS(self.maze, (self.pawn[1][0] * 2 + 1, self.pawn[1][1] * 2 + 1), (1, i * 2 + 1)) > 0:
                player2_closed = False
                break
        if player1_closed or player2_closed:
            self.maze = before_maze
        return player1_closed or player2_closed

    def undo_move(self, direction, pawn):
        undo_actions = {
            1: (-1, 0), 2: (0, 1), 3: (1, 0), 4: (0, -1),
            5: (-2, 0), 6: (0, 2), 7: (2, 0), 8: (0, -2),
            9: (-1, -1), 10: (-1, 1), 11: (1, 1), 12: (1, -1),
            13: (1, 1), 14: (1, -1), 15: (-1, -1), 16: (-1, 1)
        }
        if direction in undo_actions:
            dx, dy = undo_actions[direction]
            self.pawn[pawn - 1][0] += dx
            self.pawn[pawn - 1][1] += dy

    def is_opponent_blocked(self, pawn):
        opponent_pawn = 1 if pawn == 2 else 2
        original_position = self.pawn[opponent_pawn - 1].copy()
        for direction in range(1, 17):
            if self.move_player(direction, opponent_pawn):
                self.undo_move(direction, opponent_pawn)
                self.pawn[opponent_pawn - 1] = original_position
                return False
        self.pawn[opponent_pawn - 1] = original_position
        return True