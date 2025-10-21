from state import TutrisState
from pieces import *
from tutrisworld import TutrisWorld
from search import *
import sys, time

# Parameters of the problem
init_list1 = [PieceBar(1,7), PieceL(1,3), PieceS(4,6), PieceSquare(0,4)]
init_list2 = [PieceBar(4,6), PieceL(1,5), PieceS(5,4), PieceSquare(0,3)]
init_list3 = [PieceBar(4,6), PieceL(1,5), PieceS(3,4), PieceSquare(4,2)]

goal_list = [PieceBar(2,7), PieceL(0,5), PieceS(5,6), PieceSquare(0,6)]

init_state = TutrisState(init_list1)  # Initial state of the problem
goal_state = TutrisState(goal_list)   # Goal state of the problem


# Consistency checks
for i in range(len(init_state.piece_list)):
    if init_state.piece_list[i].__class__ != goal_state.piece_list[i].__class__:
        raise Exception("Initial and final states include different piece classes")
        
if not init_state.is_valid():
    print("Invalid initial state")
    sys.exit(0)

if not goal_state.is_valid():
    print("Invalid final state")
    sys.exit(0)
    

#------------------------------------------------------------

# Breadth First Search algorithm
start = time.perf_counter()
solution_bf, expanded, generated = breadth_first(init_state, goal_state)
end = time.perf_counter()
if solution_bf != None:
    print("breadth_first found a solution after %.2f seconds..." % (end - start))
else:
    print("breadth_first failed after %.2f seconds..." % (end - start))
show_solution(solution_bf, expanded, generated)

# Depth First Search algorithm
start = time.perf_counter()
solution_df, expanded, generated = depth_first(init_state, goal_state)
end = time.perf_counter()
if solution_df != None:
    print("depth_first found a solution after %.2f seconds..." % (end - start))
else:
    print("depth_first failed after %.2f seconds..." % (end - start))
show_solution(solution_df, expanded, generated)

# Uniform Cost Search algorithm
start = time.perf_counter()
solution_uc, expanded, generated = uniform_cost(init_state, goal_state)
end = time.perf_counter()
if solution_uc != None:
    print("uniform_cost found a solution after %.2f seconds..." % (end - start))
else:
    print("uniform_cost failed after %.2f seconds..." % (end - start))
show_solution(solution_uc, expanded, generated)

#------------------------------------------------------------

# greedy Search algorithm
start = time.perf_counter()
solution_greedy, expanded, generated = greedy(init_state, goal_state, h1)
end = time.perf_counter()
if solution_greedy != None:
    print("greedy (h1) found a solution after %.2f seconds..." % (end - start))
else:
    print("greedy (h1) failed after %.2f seconds..." % (end - start))
show_solution(solution_greedy, expanded, generated)

# A* Search algorithm (h1)
start = time.perf_counter()
solution_astar, expanded, generated = a_star(init_state, goal_state, h1)
end = time.perf_counter()
if solution_astar != None:
    print("A* (h1) found a solution after %.2f seconds..." % (end - start))
else:
    print("A* (h1) failed after %.2f seconds..." % (end - start))
show_solution(solution_astar, expanded, generated)

# Compare Greedy and A* with h_man heuristic
start = time.perf_counter()
solution_greedy_hm, expanded_gm, generated_gm = greedy(init_state, goal_state, h_man)
end = time.perf_counter()
if solution_greedy_hm != None:
    print("greedy (h_man) found a solution after %.2f seconds..." % (end - start))
else:
    print("greedy (h_man) failed after %.2f seconds..." % (end - start))
show_solution(solution_greedy_hm, expanded_gm, generated_gm)

start = time.perf_counter()
solution_astar_hm, expanded_am, generated_am = a_star(init_state, goal_state, h_man)
end = time.perf_counter()
if solution_astar_hm != None:
    print("A* (h_man) found a solution after %.2f seconds..." % (end - start))
else:
    print("A* (h_man) failed after %.2f seconds..." % (end - start))
show_solution(solution_astar_hm, expanded_am, generated_am)

#------------------------------------------------------------

# Steps for the TutrisWorld
solution = solution_bf
steps = []
while solution != None:
    if solution.action != None:
        steps.insert(0, solution.action)
    solution = solution.parent

# Possible solution to init_list1   
#steps = [(1, 'LEFT'), (2, 'RIGHT'), (0, 'RIGHT'), (3, 'DOWN'), (1, 'DOWN'), (3, 'DOWN'), (1, 'DOWN')]
try:
    world = TutrisWorld(init_state, goal_state, steps)
except Exception as ex:
    print("Error in TutrisWorld -->", ex.message)

def h1(current_state, goal_state):
    total_distance = 0
    # Calcular distancia Manhattan para cada pieza
    for i in range(len(current_state.piece_list)):
        current_piece = current_state.piece_list[i]
        goal_piece = goal_state.piece_list[i]
        # Distancia Manhattan = |x1-x2| + |y1-y2|
        distance = abs(current_piece.x - goal_piece.x) + abs(current_piece.y - goal_piece.y)
        total_distance += distance
    return total_distance

def h2(current_state, goal_state):
    # Manhattan + Importancia a piezas grandes 
    total_distance = 0
    weights = {'PieceBar': 2.0, 'PieceL': 1.75, 'PieceS': 1.5, 'PieceSquare': 1.25}
    
    for i in range(len(current_state.piece_list)):
        current_piece = current_state.piece_list[i]
        goal_piece = goal_state.piece_list[i]
        
        # Distancia Manhattan ponderada por tipo de pieza
        distance = (abs(current_piece.x - goal_piece.x) + 
                   abs(current_piece.y - goal_piece.y))
        weight = weights[current_piece.__class__.__name__]
        total_distance += distance * weight
        
    return total_distance

# Prueba con h1
print("\nPrueba con heurística h1:")
start = time.clock()
solution_astar_h1, expanded, generated = a_star(init_state, goal_state, h1)
end = time.clock()
if solution_astar_h1 != None:
    print("A* (h1) found a solution after %.2f seconds..." % (end - start))
else:
    print("A* (h1) failed after %.2f seconds..." % (end - start))
show_solution(solution_astar_h1, expanded, generated)

# Prueba con h2
print("\nPrueba con heurística h2:")
start = time.clock()
solution_astar_h2, expanded, generated = a_star(init_state, goal_state, h2)
end = time.clock()
if solution_astar_h2 != None:
    print("A* (h2) found a solution after %.2f seconds..." % (end - start))
else:
    print("A* (h2) failed after %.2f seconds..." % (end - start))
show_solution(solution_astar_h2, expanded, generated)


