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
goal_state = TutrisState(goal_list)   # Goal state of te problem


# Consistency checks
for i in range(len(init_state.piece_list)):
    if init_state.piece_list[i].__class__ != goal_state.piece_list[i].__class__:
        raise Exception("Initial and final states include different piece classes")
        
if not init_state.is_valid():
    print "Invalid initial state"
    sys.exit(0)

if not goal_state.is_valid():
    print "Invalid final state"
    sys.exit(0)
    

#------------------------------------------------------------

# Breadth First Search algorithm
start = time.clock()
solution_bf, expanded, generated = breadth_first(init_state, goal_state)
end = time.clock()
if solution_bf != None:
    print "breadth_first found a solution after %.2f seconds..." % (end - start)
else:
    print "breadth_first failed after %.2f seconds..." % (end - start)
show_solution(solution_bf, expanded, generated)

# Depth First Search algorithm
start = time.clock()
solution_df, expanded, generated = depth_first(init_state, goal_state)
end = time.clock()
if solution_df != None:
    print "depth_first found a solution after %.2f seconds..." % (end - start)
else:
    print "depth_first failed after %.2f seconds..." % (end - start)
show_solution(solution_df, expanded, generated)

# Uniform Cost Search algorithm
start = time.clock()
solution_uc, expanded, generated = uniform_cost(init_state, goal_state)
end = time.clock()
if solution_uc != None:
    print "uniform_cost found a solution after %.2f seconds..." % (end - start)
else:
    print "uniform_cost failed after %.2f seconds..." % (end - start)
show_solution(solution_uc, expanded, generated)

#------------------------------------------------------------

# greedy Search algorithm
start = time.clock()
solution_greedy, expanded, generated = greedy(init_state, goal_state, h1)
end = time.clock()
if solution_greedy != None:
    print "greedy found a solution after %.2f seconds..." % (end - start)
else:
    print "greedy failed after %.2f seconds..." % (end - start)
show_solution(solution_greedy, expanded, generated)

# A* Search algorithm
start = time.clock()
solution_astar, expanded, generated = a_star(init_state, goal_state, h1)
end = time.clock()
if solution_astar != None:
    print "A* found a solution after %.2f seconds..." % (end - start)
else:
    print "A* failed after %.2f seconds..." % (end - start)
show_solution(solution_astar, expanded, generated)

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
    print "Error in TutrisWorld -->", ex.message

