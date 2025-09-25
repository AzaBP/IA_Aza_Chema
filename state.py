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
        # Desempaquetar la acción
        num_pieza, movimiento = action
        # Copiar todas las piezas
        nuevas_piezas = [p.copy() for p in self.piece_list]
        # Seleccionar la pieza a mover
        pieza = nuevas_piezas[num_pieza]
        # Aplicar el movimiento
        if movimiento == 'LEFT':
            pieza.move_left()
        elif movimiento == 'RIGHT':
            pieza.move_right()
        elif movimiento == 'DOWN':
            pieza.move_down()
        else:
            return None  # Movimiento no válido
        # Crear el nuevo estado
        nuevo_estado = TutrisState(nuevas_piezas, self.max_x, self.max_y)
        # Validar el nuevo estado
        if nuevo_estado.is_valid():
            return nuevo_estado
        else:
            return None
        
    def is_valid(self):
        # Comprobar que todas las piezas están dentro de los límites y no se solapan
        all_cells = set()
        for p in self.piece_list:
            for (x, y) in p.occupied_positions():
                # Comprobar límites
                if not (0 <= x < self.max_x and 0 <= y < self.max_y):
                    return False
                # Comprobar colisión
                if (x, y) in all_cells:
                    return False
                all_cells.add((x, y))
        return True
    
    def next_states(self):
        new_states = []
        movimientos = ['LEFT', 'RIGHT', 'DOWN']
        for i in range(len(self.piece_list)):
            for mov in movimientos:
                accion = (i, mov)
                nuevo_estado = self.successor(accion)
                if nuevo_estado is not None:
                    new_states.append((nuevo_estado, accion))
        return new_states

