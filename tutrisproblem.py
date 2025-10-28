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
    print("\n --- Probando %s ---" + algorithm_name)
    start_time = time.perf_counter()
    try:
        if heuristic:
            solution, expanded, generated = algorithm(init_state, goal_state, heuristic)
        else:
            solution, expanded, generated = algorithm(init_state, goal_state)
    except Exception as e:
        print("Error durante la ejecucion de %s: %s" % (algorithm_name, str(e)))
        return None, [], 0, 0, float('inf')

    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    if solution != None:
        steps = reconstruct_path(solution)
        print("Solucion encontrada para %s en %.3f segundos" % (algorithm_name, execution_time))
        print("  Pasos: %d, Expandidos: %d, Generados: %d" % (len(steps), expanded, generated))
        #show_solution(solution, expanded, generated)####################################
        return solution, steps, expanded, generated, execution_time ######################################
    else:
        print("Solucion no encontrada para %s en %.3f segundos" % (algorithm_name, execution_time))
        print("  Expandidos: %d, Generados: %d" % (expanded, generated))
        return None, [], expanded, generated, execution_time

#------------------------------------------------------------
# CONFIGURACIÓN DE PRUEBAS
def run_complete_evaluation():
    # Initial states definition
    init_states = {
        init_list1 = [PieceBar(1,7), PieceL(1,3), PieceS(4,6), PieceSquare(0,4)]
        init_list2 = [PieceBar(4,6), PieceL(1,5), PieceS(5,4), PieceSquare(0,3)]
        init_list3 = [PieceBar(4,6), PieceL(1,5), PieceS(3,4), PieceSquare(4,2)]
    }

    # Objective state
    goal_list = [PieceBar(2,7), PieceL(0,5), PieceS(5,6), PieceSquare(0,6)]
    goal_state = TutrisState(goal_list)

    # Testing algorithms 
    algorithms = [
        (breadth_first, "Busqueda primero en anchura", None),
        (depth_first, "Busqueda primero en profundidad", None),
        (uniform_cost, "Busqueda de coste uniforme", None)
    ]

    # Heuristics for informed search 
    heuristics = [
        (h0_zero, "h0_sin_heuristica"),
        (h1_manhattan, "h1_manhattan"), 
        (h2_weighted_manhattan, "h2_manhattan_peso"),
        (h3_blocking_pieces, "h3_piezas_bloqueantes")
    ]

    # Informed algorithms
    for heuristic_func, heuristic_name in heuristics:
        algorithms.append((greedy, "Busqueda voraz (" + heuristic_name + ")", heuristic_func))
        algorithms.append((a_star, "A* (" + heuristic_name + ")", heuristic_func))

    # Complete results
    all_results = []
    best_solutions = {}

    print("=" * 50)
    print(" Evaluacion completa de algoritmos de busqueda ")
    print("=" * 50)

    #Probar con cada estado inicial
    print("\n\n" + "-" * 50)
    print(" Estado inicial: " + state_name)
    print("-" * 50)

    init_state = TutrisState(piece_list)

    for algorithm_func, algorithm_name, heuristic in algorithms:
        # Test
        solution, steps, expanded, generated, exec_time = test_algorithm(
            algorithm_func, algorithm_name, init_state, goal_state, heuristic
        )

        #Guardar resultados
        result = {
            'estado_inicial': state_name,
            'algoritmo': algorithm_name,
            'heuristica': heuristic.__name__ if heuristic else "N/A",
            'solucion_encontrada': solution is not None,
            'pasos_solucion': len(steps) if solution else 0,
            'nodos_expandidos': expanded,
            'nodos_generados': generated,
            'tiempo_ejecucion': exec_time,
            'tiene_solucion_visualizable': solution is not None and len(steps) > 0
        }
        all_results.append(result)

        # Guardar mejor solucion para visualizacion
        if solution and len(steps) > 0:
            key = state_name + "_" + algorithm_name.replace(' ', '_')
            if key not in best_solutions or len(steps) < len(best_solutions[key]['steps']):
                best_solutions[key] = {
                    'algorithm': algorithm_name,
                    'steps': steps,
                    'state_name': state_name,
                    'init_state': init_state,
                    'goal_state': goal_state,
                    'pasos': len(steps)
                    'expandidos': expanded
                }

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