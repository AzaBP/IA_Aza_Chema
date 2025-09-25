# This module defines the classes Piece, PieceBar, PieceL, PieceS and PieceSquare
#--------------------------------------------------------------------------------

class Piece:
    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_down(self):
        self.y += 1
    """
    Class representing the pieces of the Tutris World
    """
    def __init__(self, x=0, y=0):
        self.x = x 
        self.y = y
        self.symbol = ' '
        self.shape = []

    def occupied_positions(self):
        # Devuelve las posiciones absolutas ocupadas por la pieza
        return [(self.x + dx, self.y + dy) for (dx, dy) in self.shape]
    
    def apply_movement(self, movement):
        if movement == 'LEFT':
            self.x -= 1
        elif movement == 'RIGHT':
            self.x += 1
        elif movement == 'DOWN':
            self.y += 1
    
    def copy(self):
        return None
    
    def __eq__(self, other):
        if other:
            return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y
        else:
            return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return "%s(%d,%d)" % (self.__class__.__name__, self.x, self.y)
    
    def draw(self, board):
        for (x,y) in self.occupied_positions():
            board[y][x] = self.symbol
        return board
    

class PieceBar(Piece):
    """
    Piece with the shape of a horizontal bar

    xx xx xx xx
    xx xx xx xx

    """
    def __init__(self, x=0, y=0):
        self.x = x 
        self.y = y
        self.symbol = '+'
        self.shape = [(0,0), (1,0), (2,0), (3,0)]

    def copy(self):
        return PieceBar(self.x, self.y)
    

class PieceL(Piece):
    """
    Piece with L-shape
    
    xx xx xx
    xx xx xx
          xx
          xx
          
    """
    def __init__(self, x=0, y=0):
        self.x = x 
        self.y = y
        self.symbol = '*'
        self.shape = [(0,0), (1,0), (2,0), 
                                    (2,1)]

    def copy(self):
        return PieceL(self.x, self.y)


class PieceS(Piece):
    """
    Piece with S-shape

    xx xx
    xx xx
       xx xx
       xx xx

    """
    def __init__(self, x=0, y=0):
        self.x = x 
        self.y = y
        self.symbol = '#'
        self.shape = [(0,0), (1,0), 
                             (1,1), (2,1)]

    def copy(self):
        return PieceS(self.x, self.y)
    
    
class PieceSquare(Piece):
    """
    Piece with Square shape

    xx xx
    xx xx
    xx xx
    xx xx

    """
    def __init__(self, x=0, y=0):
        self.x = x 
        self.y = y
        self.symbol = '%'
        self.shape = [(0,0), (1,0), 
                      (0,1), (1,1)]

    def copy(self):
        return PieceSquare(self.x, self.y)
