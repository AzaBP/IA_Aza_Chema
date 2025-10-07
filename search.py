from datastructures import *

#----------------------------------------------------------------------

class Node:
    """
    This class is used to represent nodes of the search tree.  Each
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
    frontier.push(initial_node)
    explored = set()
    while not frontier.is_empty():
        node = frontier.pop()
        if node.state == goal_state:
            return (node, expanded, generated)
        explored.add(node.state)
        expanded += 1
        for child in node.expand():
            if (child.state not in explored) and (not frontier.contains_state(child.state)):
                frontier.push(child)
                generated += 1
    return (None, expanded, generated)
    
#----------------------------------------------------------------------
# Test functions for uninformed search

def breadth_first(initial_state, goal_state):
    frontier = Queue()
    frontier.push = frontier.insert
    frontier.pop = frontier.remove
    frontier.contains_state = lambda state: frontier.contains(Node(state, None, None))
    return uninformed_search(initial_state, goal_state, frontier)

def depth_first(initial_state, goal_state):
    frontier = Stack()
    frontier.push = frontier.insert
    frontier.pop = frontier.remove
    frontier.contains_state = lambda state: frontier.contains(Node(state, None, None))
    return uninformed_search(initial_state, goal_state, frontier)

def uniform_cost(initial_state, goal_state):
    frontier = PriorityQueue(lambda node: node.g)
    frontier.push = frontier.insert
    frontier.pop = frontier.remove
    frontier.contains_state = lambda state: frontier.contains(Node(state, None, None))
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

def h1(current_state, goal_state):
    return 0


def h_man(current_state, goal_state):
    """Heurística Manhattan por pieza.

    Para cada pieza en current_state se toma la posición de referencia (x,y)
    y la posición correspondiente en goal_state (mismo índice de lista).
    La heurística es la suma de las distancias Manhattan |dx|+|dy|.
    """
    h = 0
    for i in range(len(current_state.piece_list)):
        p_curr = current_state.piece_list[i]
        p_goal = goal_state.piece_list[i]
        # Usamos la referencia (x,y) de cada pieza
        dx = abs(p_curr.x - p_goal.x)
        dy = abs(p_curr.y - p_goal.y)
        h += dx + dy
    return h


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

