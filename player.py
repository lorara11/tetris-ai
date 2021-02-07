from board import Direction, Rotation
from random import Random


class Player:
    def __init__(self):
        heights = []    # heights for each column
        chosen_position = -999999
        chosen_rotation = -999999

    # I define functions that will be used to calculate the score of the sandbox

    def calculate_heights(self, board):
        self.heights = [0] * board.width
        for x in range(board.width):
            for y in range(board.height, 0, -1):
                if (x, y) in board.cells:
                    self.heights[x] = board.height - y


    def sum_of_heights(self, board):
        self.calculate_heights(board)
        return sum(self.heights)


    def holes_count(self, board):
        total_holes = 0
        for x in range (board.width):   # iterate through columns
            for y in range(board.height):    # iterate through each row in column
                if (x,y) not in board.cells:
                    if (x, y+1) in board.cells and (x, y-1) in board.cells and (x+1, y) in board.cells and (x-1, y) in board.cells:  # check if it's a hole
                        total_holes += 1

                    if (x, y+1) not in board.cells and (x,y+2) in board.cells and (x, y-1) in board.cells and (x+1, y) in board.cells and (x-1, y) in board.cells and (x+1, y+1) in board.cells and (x-1, y+1) in board.cells:  # check if it's a double hole
                        total_holes += 1
                    if (x, y+1) in board.cells and (x, y-1) not in board.cells and (x,y-2) in board.cells and (x+1, y) in board.cells and (x-1, y) in board.cells and (x+1, y-1) in board.cells and (x-1, y-1) in board.cells:
                        total_holes += 1
                    if (x, y+1) in board.cells and (x, y-1) in board.cells and (x+1, y) not in board.cells and (x+2,y) in board.cells and (x-1, y) in board.cells and (x+1, y+1) in board.cells and (x+1, y-1) in board.cells:
                        total_holes += 1
                    if (x, y+1) in board.cells and (x, y-1) in board.cells and (x+1, y) in board.cells and (x-1, y) not in board.cells and (x-2,y) in board.cells and (x-1, y+1) in board.cells and (x-1, y-1) in board.cells:
                        total_holes += 1
                    
        return total_holes


    def calculate_bumpiness(self, board):
        bumpiness = 0
        self.calculate_heights(board)
        for i in range(board.width -1 ):
            bumpiness += abs(self.heights[i+1] - self.heights[i])
        return bumpiness


    def count_cleared_lines(self, board, previous_score):
        new_score = board.score
        diff = new_score - previous_score

        if diff >= 1600:
            return 4
        elif diff >= 800:
            return 3
        elif diff >= 400:
            return 2
        elif diff >= 100:
            return 1
        else:
            return 0


    def find_best_move(self,board):
        weight_sum_heigths = -0.510066       # optimal parameters calculated using genetic algorithm
        weight_holes = -0.35663
        weight_bumpiness = -0.184483
        weight_cleared_lines = 0.760666
        
        current_score, best_score = 0.0, -999999

        for rotation in range(0,4):     # iterating through all possible clockwise rotations
            for position in range(0,board.width):   # iterating through all possible positions of block
                sandbox = board.clone()    # here we'll do experiments to find the best score possible
                
                for i in range(0, rotation):        # rotate block
                    try:
                        if sandbox.falling is not None:
                            sandbox.rotate(Rotation.Clockwise)
                    except:
                        pass

                if position < 5:        # move block left 
                    for i in range(0, 5-position):
                        try:
                            if sandbox.falling is not None:
                                sandbox.move(Direction.Left)
                        except:
                            pass
                else:                   # move block right
                    for i in range(0, position-4):
                        try:
                            if sandbox.falling is not None:
                                sandbox.move(Direction.Right)
                        except:
                            pass
                
                try:        # block is in the right position, with the right rotation. Move block down
                    sandbox.move(Direction.Drop)
                except:
                    pass
                
                current_score = weight_sum_heigths * self.sum_of_heights(sandbox) + weight_holes * self.holes_count(sandbox) + weight_bumpiness * self.calculate_bumpiness(sandbox) + weight_cleared_lines * self.count_cleared_lines(sandbox, board.score)

                if current_score > best_score:
                    best_score, self.chosen_position, self.chosen_rotation = current_score, position, rotation


    def choose_action(self, board):
        self.find_best_move(board)
        
        moves_return = []

        for i in range(0,self.chosen_rotation):           # rotate block
            moves_return.append(Rotation.Clockwise)

        if self.chosen_position < 5:       # move block to right position
            for i in range(0, 5-self.chosen_position):
                moves_return.append(Direction.Left)
        else:
            for i in range(0, self.chosen_position-4):
                moves_return.append(Direction.Right)

        if board.falling is not None:
            moves_return.append(Direction.Drop)
        
        return moves_return



class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        return self.random.choice([
            Direction.Left,
            Direction.Right,
            Direction.Down,
            Rotation.Anticlockwise,
            Rotation.Clockwise,
        ])


SelectedPlayer = Player


