# This module defines the classes Piece, PieceBar, PieceL, PieceS and PieceSquare
#--------------------------------------------------------------------------------

class Piece:
    """
    Class representing the pieces of the Tutris World
    """
    def __init__(self, x=0, y=0):
        self.x = x 
        self.y = y
        self.symbol = ' '
        self.shape = []
        
    def occupied_positions(self):
        """
        Rellenar con el codigo necesario para generar una lista con las posiciones
        ocupadas con una pieza teniendo en cuenta su situacion (self.x, self.y) y
        la forma de la pieza (reflejada en la lista self.shape)
        Ejemplos:
          PieceBar(2,4)    --> [(2, 4), (3, 4), (4, 4), (5, 4)]
          PieceL(1,5)      --> [(1, 5), (2, 5), (3, 5), (3, 6)]
          PieceS(0,1)      --> [(0, 1), (1, 1), (1, 2), (2, 2)]
          PieceSquare(3,3) --> [(3, 3), (4, 3), (3, 4), (4, 4)]
        """
        return []
    
    def apply_movement(self, movement):
        """
        Rellenar con el codigo necesario para modificar la posicion de la pieza
        segun los movimientos 'LEFT', 'RIGHT' y 'DOWN'. La funcion no debe 
        devolver nada (es decir, no debe tener una clausula return)
        Ejemplos:
          PieceBar(2,4) + 'LEFT'  = PieceBar(1,4)
          PieceBar(2,4) + 'RIGHT' = PieceBar(3,4)
          PieceBar(2,4) + 'DOWN'  = PieceBar(2,5)
        """
    
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
