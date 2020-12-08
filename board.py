from enum import Enum
from collections import namedtuple

class Color(Enum):
    white = 0
    black = 1

class Position(namedtuple("Position", ['x', 'y'])):
    # self + to = new Position
    def __add__(self, to):
        return Position(self.x+to[0], self.y+to[1])

class ErrorNotDefined(Exception): pass

def filter_valid_pos(moves: [Position]) -> [Position]:
    return filter(lambda p: p.x >= 1 and p.x <= 8 and p.y >= 1 and p.y <= 8, moves)

class Piece:
    def __init__(self, pos: Position, color: Color):
        self.color = color
        self.pos = pos

    def potential_move(self) -> [Position]:
        raise ErrorNotDefined()

class Pawn(Piece):
    def potential_move(self):
        delta = +1 if self.color == Color.white else -1
        result = [self.pos + (0, delta * +1)]
        if self.pos.y == 2 * delta:
            result.append(self.pos + (0, delta * +2))
        result1 = [
            self.pos + (-1, delta * +1),
            self.pos + (+1, delta * +1),
        ]
        return filter_valid_pos(result + result1)

class King(Piece):
    def potential_move(self):
        result = [self.pos + (i, j) \
            for i in [-1, 0, +1]
            for j in [-1, 0, +1]
            if not (i == 0 and j == 0)]
        return filter_valid_pos(result)
        

class Queen(Piece):
    def potential_move(self):
        result_horizental = [self.pos + (i, 0) for i in range(-8, 8) if i!=0]
        result_vertical = [self.pos + (0, j) for j in range(-8, 8) if j!=0]
        result_diagnol0 = [self.pos + (i,i) for i in range(-10, 10)]
        result_diagnol1 = [self.pos + (i,-i) for i in range(-10, 10)]
        result = filter_valid_pos(
            result_horizental + result_vertical + 
            result_diagnol0 + result_diagnol1)
        return result

class Rook(Piece):
    def potential_move(self):
        result0 = [self.pos + (i, 0) \
            for i in range(-10, 10) if i != 0]
        result1 = [self.pos + (0, j) \
            for j in range(-10, 10) if j != 0]
        return filter_valid_pos(result0 + result1)

class Bishop(Piece):
    def potential_move(self):
        result_diagnol0 = [self.pos + (i, i) \
            for i in range(-10, 10) if i != 0]
        result_diagnol1 = [self.pos + (-i, i) \
            for i in range(-10, 10) if i != 0]
        return filter_valid_pos(result_diagnol0 + result_diagnol1)

class Knight(Piece):
    def potential_move(self):
        result = [self.pos + delta for delta in [
            (-2, +1), (-1, +2), (+1, +2), (+2, +1),
            (-2, -1), (-1, -2), (+1, -2), (+2, -1)]]
        return filter_valid_pos(result)

class Board:
    def __init__(self):
        # Initiation board.
        # self.white_pieces = [None] * 16
        # self.black_pieces = [None] * 16
        self.board = [[None] * 8 for _ in range(8)]
