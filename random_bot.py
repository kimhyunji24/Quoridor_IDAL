from random import sample, uniform

class Random_Bot:
    def __init__(self, board, name=''):
        self.pawn = None
        self.board = board
        self.name = name
        self.score = 0

    def set_pawn(self, pawn):
        self.pawn = pawn

    def play(self):
        done = False
        while not done:
            threshold = 0.9
            if uniform(0,1)<=threshold:
                pos_dir = self.board.search_direction(self.pawn)
                if len(pos_dir) > 0:
                    dir = sample(pos_dir, 1)[0]
                    done = self.board.move_player(dir, self.pawn)
            else:
                r = sample(range(self.board.rows), 1)[0]
                c = sample(range(self.board.cols), 1)[0]
                d = sample(range(0,2), 1)[0]+1
                done = self.wall(r,c,d)


    def move(self, direction):
        res = self.board.move_player(direction, self.pawn)
        return res

    def wall(self, r, c, direction):
        res = self.board.put_wall(r,c,direction,self.pawn)
        return res