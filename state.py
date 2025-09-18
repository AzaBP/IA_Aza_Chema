from pieces import *

class TutrisState:
    """
    State of the Tutris game
    Each object contains a list with the pieces included
    """    
    def __init__(self, piece_list, max_x=8, max_y=8):
        self.piece_list = piece_list
        self.max_x = max_x
        self.max_y = max_y
        
    def __str__(self):
        board = [[' ' for i in range(self.max_x)] for j in range(self.max_y)]
        for p in self.piece_list:
            p.draw(board)
        return '\n'.join([('| ' + ' '.join(row) + ' |') for row in board])
        
    def __eq__(self, other):
        if other:
            for i in range(len(self.piece_list)):
                if self.piece_list[i] != other.piece_list[i]:
                    return False
            return True
        else:
            return False
    
    
    def successor(self, action):
        
        """
        Rellenar con el codigo necesario para generar un nuevo estado a partir del actual
        y una accion proporcionada como parametro. La accion tiene el formato 
        (<num_pieza>, <movimiento>), donde <num_pieza> es un numero entero indicando la
        pieza a mover, y <movimiento> puede ser 'LEFT', 'RIGHT' o 'DOWN'. La funcion debe 
        devolver None si el estado generado es invalido segun las especificaciones del problema
        NOTA: las piezas del estado actual no deben usarse directamente en el estado objetivo,
        sino realizar copias de las mismas mediante el metodo copy()
        """
        return None
        
    def is_valid(self):
        """
        Rellenar con el codigo necesario para determinar si un estado es valido. Se consideran
        validos aquellos estados en los que las piezas no intersectan entre si y todas ellas
        estan situadas en los limites del escenario (delimitado por [0..max_x-1][0..max_y-1])
        NOTA: puede ser interesante utilizar los conjuntos (set) de Python para comprobar las
        colisiones entre piezas
        """
        return True
    
    def next_states(self):
        new_states = []

        """
        Rellenar con el codigo necesario para generar la lista de nuevos estados accesibles
        desde el estado actual, aplicando las diferentes acciones posibles. Los estados deben 
        ser validos segun las especificaciones del problema. La lista debe estar formada por 
        pares (nuevo_estado, accion)
        """
        return new_states

