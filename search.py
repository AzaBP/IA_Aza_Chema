from datastructures import *

#----------------------------------------------------------------------

class Node:
    """
    This class is used to represent nodes of the search tree. Each
    node contains a state representation, a reference to the node's
    parent node, a string that describes the action that generated
    the node's state from the parent state, and the path cost g from
    the start node to this node.
    """
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        if other:
            return self.state == other.state
        else:
            return False
    
    def expand(self):
        successors = []
        for (new_state, action) in self.state.next_states():
            new_node = Node(new_state, self, action)
            # Update path cost: each move has unit cost
            new_node.g = self.g + 1
            successors.append(new_node)
        return successors

#----------------------------------------------------------------------

def uninformed_search(initial_state, goal_state, frontier):
    """
    Parametros:
       initial_state: estado inicial de busqueda (objeto de clase TutrisState)
       goal_state: estado inicial de busqueda (objeto de clase TutrisState)
       frontier: estructura de datos para contener los estados de la frontera (objeto de clase
           contenida en el modulo DataStructures)
    """

    initial_node = Node(initial_state, None, None)
    expanded = 0
    generated = 0
    frontier.insert(initial_node)
    explored = set()
    while not frontier.is_empty():
        node = frontier.remove()
        # Sin la comprobación da errores en ejecución
        if node is None:
            return (None, expanded, generated)
        if node.state == goal_state:
            return (node, expanded, generated)
        explored.add(node.state)
        expanded += 1
        for child in node.expand():
            # Evitar problemas de ejecucion
            contents = getattr(frontier, 'contents', [])
            in_frontier = any((n is not None and n.state == child.state) for n in contents)
            if child.state not in explored and not in_frontier:
                frontier.insert(child)
                generated += 1
    return (None, expanded, generated)
    
#----------------------------------------------------------------------
# Test functions for uninformed search

def breadth_first(initial_state, goal_state):
    frontier = Queue()
    frontier.push = frontier.insert
    frontier.pop = frontier.remove
    frontier.is_empty = frontier.is_empty
    frontier.contains_state = lambda state: any (
        node.state == state for node in frontier.contents if hasattr (frontier, 'contents')
    )
    return uninformed_search(initial_state, goal_state, frontier)

def depth_first(initial_state, goal_state):
    frontier = Stack()
    frontier.push = frontier.insert
    frontier.pop = frontier.remove
    frontier.contains_state = lambda state: any(
        node.state == state for node in frontier.contents if hasattr(frontier, 'contents')
    )
    return uninformed_search(initial_state, goal_state, frontier)

def uniform_cost(initial_state, goal_state):
    frontier = PriorityQueue(lambda node: node.g)
    frontier.push = frontier.insert
    frontier.pop = frontier.remove
    frontier.contains_state = lambda state: any(
        node.state == state for node in frontier.contents if hasattr(frontier, 'contents')
    ) and frontier.contents
    return uninformed_search(initial_state, goal_state, frontier)


#----------------------------------------------------------------------

def informed_search(initial_state, goal_state, frontier, heuristic):
    """
    Parametros:
       initial_state: estado inicial de busqueda (objeto de clase TutrisState)
       goal_state: estado inicial de busqueda (objeto de clase TutrisState)
       frontier: estructura de datos para contener los estados de la frontera (objeto de clase
           contenida en el modulo DataStructures)
       heuristic: funcion heuristica utilizada para guiar el proceso de busqueda. La
           funcion recibe dos parametros (estado actual y estado objetivo) y devuelve
           una estimacion de coste entre ambos estados
    """

    initial_node = Node(initial_state, None, None)
    initial_node.h = heuristic(initial_state, goal_state)
    expanded = 0
    generated = 0
    frontier.push(initial_node)
    explored = set()
    while not frontier.is_empty():
        node = frontier.pop()
        # Sin la comprobación da errores en ejecución
        if node is None:
            return (None, expanded, generated)
        if node.state == goal_state:
            return (node, expanded, generated)
        explored.add(node.state)
        expanded += 1
        for child in node.expand():
            child.h = heuristic(child.state, goal_state)
            if (child.state not in explored) and (not frontier.contains_state(child.state)):
                frontier.push(child)
                generated += 1
    return (None, expanded, generated)
    
#----------------------------------------------------------------------
# Test functions for informed search

def greedy(initial_state, goal_state, heuristic):
    frontier = PriorityQueue(lambda node: node.h)
    frontier.push = frontier.insert
    frontier.pop = frontier.remove
    frontier.contains_state = lambda state: frontier.contains(Node(state, None, None))
    return informed_search(initial_state, goal_state, frontier, heuristic)

def a_star(initial_state, goal_state, heuristic):
    frontier = PriorityQueue(lambda node: node.g + node.h)
    frontier.push = frontier.insert
    frontier.pop = frontier.remove
    frontier.contains_state = lambda state: frontier.contains(Node(state, None, None))
    return informed_search(initial_state, goal_state, frontier, heuristic)

#---------------------------------------------------------------------
# Heuristic functions

def h0_zero(current_state, goal_state): 
    return 0 # Equivalente a busqueda no informada

def h1_manhattan(current_state, goal_state):
    total_distance = 0
    # Calcular distancia Manhattan para cada pieza
    for i in range(len(current_state.piece_list)):
        current_piece = current_state.piece_list[i]
        goal_piece = goal_state.piece_list[i]
        # Distancia Manhattan = |x1-x2| + |y1-y2|
        distance = (abs(current_piece.x - goal_piece.x) + 
                    abs(current_piece.y - goal_piece.y))
        total_distance += distance
    return total_distance

def h2_weighted_manhattan(current_state, goal_state):
    # Manhattan + Importancia a piezas grandes 
    total_distance = 0
    weights = {'PieceBar': 2.0, 'PieceL': 1.75, 'PieceS': 1.5, 'PieceSquare': 1.25}
    for i in range(len(current_state.piece_list)):
        current_piece = current_state.piece_list[i]
        goal_piece = goal_state.piece_list[i]
        # Distancia Manhattan ponderada por tipo de pieza
        distance = (abs(current_piece.x - goal_piece.x) + 
                    abs(current_piece.y - goal_piece.y))
        weight = weights.get(current_piece.__class__.__name__, 1.0)
        total_distance += distance * weight
    return total_distance

def h3_blocking_pieces(current_state, goal_state):
    """
    Heurística 3: Cuenta piezas que están en el camino de otras
    """
    blocking_count = 0
    current_positions = set()
    
    # Obtener todas las posiciones ocupadas en estado actual
    for piece in current_state.piece_list:
        current_positions.update(piece.occupied_positions())
    
    # Para cada pieza, verificar si su camino al objetivo está bloqueado
    for i in range(len(current_state.piece_list)):
        current_piece = current_state.piece_list[i]
        goal_piece = goal_state.piece_list[i]
        
        # Si la pieza necesita moverse horizontalmente
        if current_piece.x != goal_piece.x:
            # Verificar si hay piezas en el camino horizontal
            step_x = 1 if goal_piece.x > current_piece.x else -1
            for x in range(current_piece.x + step_x, goal_piece.x, step_x):
                temp_positions = [(x + dx, current_piece.y + dy) for (dx, dy) in current_piece.shape]
                if any(pos in current_positions for pos in temp_positions):
                    blocking_count += 1
                    break
        
        # Si la pieza necesita moverse verticalmente  
        if current_piece.y != goal_piece.y:
            # Verificar si hay piezas en el camino vertical
            step_y = 1 if goal_piece.y > current_piece.y else -1
            for y in range(current_piece.y + step_y, goal_piece.y, step_y):
                temp_positions = [(current_piece.x + dx, y + dy) for (dx, dy) in current_piece.shape]
                if any(pos in current_positions for pos in temp_positions):
                    blocking_count += 1
                    break
    
    return blocking_count

#----------------------------------------------------------------------

def show_solution(node, expanded, generated):
    path = []
    while node != None:
        path.insert(0, node)
        node = node.parent
    if path:
        print("Solution took %d steps" % (len(path) - 1))
        print(path[0].state)
        for n in path[1:]:
            print(n.action)
            print(n.state)
    print("Nodes expanded:  %d" % expanded)
    print("Nodes generated: %d\n" % generated)

