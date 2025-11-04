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
        "init_list1": [PieceBar(1,7), PieceL(1,3), PieceS(4,6), PieceSquare(0,4)],
        "init_list2": [PieceBar(4,6), PieceL(1,5), PieceS(5,4), PieceSquare(0,3)],
        "init_list3": [PieceBar(4,6), PieceL(1,5), PieceS(3,4), PieceSquare(4,2)]
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
    heuristics = [h0_zero, h1_manhattan, h2_weighted_manhattan, h3_blocking_pieces]    
    for heuristic_func in heuristics:
        heuristic_name = heuristic_func.__name__
        algorithms.append((greedy, "Busqueda voraz (" + heuristic_name + ")", heuristic_func))
        algorithms.append((a_star, "A* (" + heuristic_name + ")", heuristic_func))

    # Complete results
    all_results = []
    best_solutions = {}

    print("=" * 50)
    print(" Evaluacion completa de algoritmos de busqueda ")
    print("=" * 50)

    #Probar con cada estado inicial
    for state_name, piece_list in init_states.items():
        print("\n\n" + "-" * 50)
        print(" Estado inicial: " + state_name)
        print("-" * 50)

        init_state = TutrisState(piece_list)

        for algorithm_func, algorithm_name, heuristic in algorithms:
            # Test algorithm
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
                        'pasos': len(steps),
                        'expandidos': expanded
                    }

    generate_report(all_results, best_solutions)
    return all_results, best_solutions

def generate_report(results, best_solutions):
    # Generates detailed report of results
    print("\n\n" + "=" * 50)
    print(" RESUMEN DE RESULTADOS ")
    print("=" * 50)

    print("\nResumen por algoritmo: " + "-" * 27)
    algorithm_results = {}
    for result in results:
        algo = result['algoritmo']
        if algo not in algorithm_results:
            algorithm_results[algo] = []
        algorithm_results[algo].append(result)
    
    # Print summary per algorithm
    for algorithm_name, algorithm_data in algorithm_results.items():
        solutions_found = sum(1 for rresult in algorithm_data if result['solucion_encontrada'])
        total_tests = len(algorithm_data)
        avg_steps = sum(result['pasos_solucion'] for result in algorithm_data if result['solucion_encontrada']) / solutions_found if solutions_found > 0 else 0
        avg_expanded = sum(result['nodos_expandidos'] for result in algorithm_data) / total_tests
        avg_time = sum(result['tiempo_ejecucion'] for result in algorithm_data) / total_tests

        print("\n" + algorithm_name + ":")
        print("  Soluciones encontradas: %d/%d (%.1f%%)" % (solutions_found, total_tests, (solutions_found / total_tests) * 100))
        print("  Pasos promedio: %.1f" % avg_steps)
        print("  Nodos expandidos promedio: %.1f" % avg_expanded)
        print("  Tiempo de ejecucion promedio: %.3f segundos" % avg_time)

    # Best solutions found
    print("\nMEJORES SOLUCIONES ENCONTRADAS " + '-' * 19)
    for key, solution in best_solutions.items():
        print("  " + solution['algorithm'] + " (" + solution['state_name'] + "): " + 
              str(solution['pasos']) + " pasos, " + str(solution['expandidos']) + " nodos expandidos")
        
    # Save results in file
    filename = "res_p1_ia.txt"
    with open(filename, 'w') as f:
        f.write("RESULTADOS BUSQUEDA TUTRIS\n")
        f.write("=" * 50 + "\n")
        for result in results:
            f.write("Algoritmo: %s\n" % result['algoritmo'])
            f.write("Estado: %s, Solución: %s\n" % (result['estado_inicial'], "SÍ" if result['solucion_encontrada'] else "NO"))
            f.write("Pasos: %d, Expandidos: %d, Generados: %d, Tiempo: %.4f\n" % (
                result['pasos_solucion'],
                result['nodos_expandidos'],
                result.get('nodos_generados', 0),
                result['tiempo_ejecucion']
            ))
            f.write("-" * 30 + "\n")
    
    print("\nResultados guardados en: " + filename)
    return results

def visualize_solution(solution):
    # Visualices a specific solution
    try:
        print("Ejecutando visualizacion con %d pasos..." % len(solution['steps']))
        world = TutrisWorld(
            solution['init_state'], 
            solution['goal_state'],
            solution['steps']
        )
    except Exception as e:
        print("Error durante la visualizacion: %s" % str(e))

#------------------------------------------------------------
# MAIN PROGRAM
if __name__ == "__main__":
    print("=" * 80)
    print(" PRACTICA 1: ALGORITMOS DE BUSQUEDA ")
    print("=" * 80)
    
    try:
        # Execute complete evaluation
        all_results, best_solutions = run_complete_evaluation()

        # Show visualization
        # for key, solution in best_solutions.items(): ########################################
        #     visualize_solution(solution)              ########################################

        print("Evaluacion completa finalizada.")
        print("Revisa el archivo 'res_p1_ia.txt' para el resumen de resultados.")
    
    except Exception as e:
        print("Error durante la evaluacion: %s" % str(e))
        import traceback
        traceback.print_exc()

