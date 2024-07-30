from board import Board

class Player:
    def __init__(self, board, name=''):
        self.pawn = None
        self.board = board
        self.name = name
        self.score = 0

    def set_pawn(self, pawn):
        self.pawn = pawn

    def play(self):
        """Win the game"""
        return

    def move(self, direction):
        res = self.board.move_player(direction, self.pawn)
        return res

    def wall(self, r, c, direction):
        res = self.board.put_wall(r,c,direction,self.pawn)
        return res