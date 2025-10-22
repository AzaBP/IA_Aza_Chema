from state import TutrisState
from pieces import *
from tutrisworld import TutrisWorld
from search import *
import sys, time

#------------------------------------------------------------
# FUNCIONES AUXILIARES
def reconstruct_path(solution_node):
    steps = []
    current = solution_node
    while current != None:
        if current.action != None:
            steps.insert(0, current.action)
        current = current.parent
    return steps

def test_algorithm(algorithm, algorithm_name, init_state, goal_state, heuristic=None):
    print("\n --- Probando %s ---" % algorithm_name)
    start = time.perf_counter()
    if heuristic:
        solution, expanded, generated = algorithm(init_state, goal_state, heuristic)
    else:
        solution, expanded, generated = algorithm(init_state, goal_state)
    end = time.perf_counter()
    
    if solution != None:
        steps = reconstruct_path(solution)
        print("Solucion encontrada para %s en %.2f segundos" % (algorithm_name, end - start))
        print("  Pasos: %d, Expandidos: %d, Generados: %d" % (len(steps), expanded, generated))
        show_solution(solution, expanded, generated)
        return solution, steps, expanded, generated
    else:
        print("Solucion no encontrada para %s en %.2f segundos" % (algorithm_name, end - start))
        print("  Expandidos: %d, Generados: %d" % (expanded, generated))
        return None, [], expanded, generated

# Initial states
init_list1 = [PieceBar(1,7), PieceL(1,3), PieceS(4,6), PieceSquare(0,4)]
init_list2 = [PieceBar(4,6), PieceL(1,5), PieceS(5,4), PieceSquare(0,3)]
init_list3 = [PieceBar(4,6), PieceL(1,5), PieceS(3,4), PieceSquare(4,2)]

# Objective state
goal_list = [PieceBar(2,7), PieceL(0,5), PieceS(5,6), PieceSquare(0,6)]

# State definitions
init_state = TutrisState(init_list1)  # Initial state of the problem
goal_state = TutrisState(goal_list)   # Goal state of the problem

# Validaciones de consistencia
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
# TESTS WITH UNIFIED FUNCTION

print("=" * 50)
print("=" * 7 + " PRACTICA 1: ALGORITMOS DE BUSQUEDA " + "=" * 7)
print("=" * 50)

print("\n" + "=" * 35)
print("BUSQUEDAS NO INFORMADAS")
print("=" * 35)

test_algorithm(breadth_first, "Busqueda primero en anchura", init_state, goal_state)
test_algorithm(depth_first, "Busqueda primero en profundidad", init_state, goal_state)
test_algorithm(uniform_cost, "Busqueda de coste uniforme", init_state, goal_state)

print("\n\n" + "=" * 35)
print("BUSQUEDAS INFORMADAS")
print("=" * 50)

# Definir heurísticas a probar
heuristics_to_test = [
    (h0_zero, "h0_zero"),
    (h1_manhattan, "h1_manhattan"), 
    (h2_weighted_manhattan, "h2_weighted_manhattan"),
    (h3_blocking_pieces, "h3_blocking_pieces")
]

for heuristic, heuristic_name in heuristics_to_test:
    print("\n--- Heurística: %s ---" % heuristic_name)
    test_algorithm(greedy, "Busqueda voraz/primero el mejor (%s)" % heuristic_name, init_state, goal_state, heuristic)
    test_algorithm(a_star, "A* (%s)" % heuristic_name, init_state, goal_state, heuristic)

#------------------------------------------------------------

# greedy Search algorithm
start = time.perf_counter()
solution_greedy, expanded, generated = greedy(init_state, goal_state, h1_manhattan)
end = time.perf_counter()
if solution_greedy != None:
    print("greedy (h1) found a solution after %.2f seconds..." % (end - start))
else:
    print("greedy (h1) failed after %.2f seconds..." % (end - start))
show_solution(solution_greedy, expanded, generated)

# A* Search algorithm (h1)
start = time.perf_counter()
solution_astar, expanded, generated = a_star(init_state, goal_state, h1_manhattan)
end = time.perf_counter()
if solution_astar != None:
    print("A* (h1) found a solution after %.2f seconds..." % (end - start))
else:
    print("A* (h1) failed after %.2f seconds..." % (end - start))
show_solution(solution_astar, expanded, generated)

#------------------------------------------------------------
print("\n\n" + "=" * 35)
print("VISUALIZACION (Si existe solucion)")
print("=" * 35)

# Probar A* con h1_manhattan para visualización
solution, steps, expanded, generated = test_algorithm(
    a_star, "A* (h1_manhattan) - VISUAL", init_state, goal_state, h1_manhattan
)

if solution and steps:
    print("\nEjecutando visualización con %d pasos..." % len(steps))
    try:
        world = TutrisWorld(init_state, goal_state, steps)
    except Exception as ex:
        print("Error en TutrisWorld: %s" % str(ex))
else:
    print("No hay solución para visualizar")