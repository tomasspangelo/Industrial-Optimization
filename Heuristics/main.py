from utils import read_data
from vessel import Vessel
from solution import Solution

filename = './instance1.txt'

b, s, t, containers = read_data(filename)
vessel = Vessel(b, s, t)
number_of_containers = len(containers)

initial_solution = Solution(b, s, t)

initial_solution.construct()
initial_solution.calculate_objective(containers)
initial_solution.print_sol()
print(initial_solution.objective)

'''
%OPPGAVE 1
%constructionImproved(InitialSolution,Containers);
%Implementer denne i Solution.m.

%Sortere containere etter vekt kan gj�res slik:
%ContainersDescending = sortArrayWeightDescending(Containers);
%ContainersAscending = sortArrayWeightAscending(Containers);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Print the initial solution to command window
%print(InitialSolution);

%Evaluate the initial solution
'''
initial_solution = Solution(b, s, t)
initial_solution.construction_improved(containers)
initial_solution.calculate_objective(containers)
initial_solution.print_sol()
print(initial_solution.objective)



'''
%Improvement phase

%Create a copy of the initial solution.
%NewSolution=copy(InitialSolution);
'''
'''
%OPPGAVE 2A
%LocalSearchTwoSwap(NewSolution,Containers);
%Implementer denne i Solution.m.
%disp(NewSolution.objective);
'''
new_solution = initial_solution.make_copy()
new_solution.local_search_two_swap(containers)
new_solution.calculate_objective(containers)
new_solution.print_sol()
print(new_solution.objective)

"""
%OPPGAVE 2B
%LocalSearchThreeSwap(NewSolution,Containers);
%Implementer denne i Solution.m.
%disp(NewSolution.objective);
"""
new_solution = new_solution.make_copy()
new_solution.local_search_three_swap(containers)
new_solution.calculate_objective(containers)
new_solution.print_sol()
print(new_solution.objective)

'''
%OPPGAVE 3
%nIterations = 100;
%TabuSearchHeuristic(NewSolution,Containers,nIterations);
%disp(NewSolution.objective);
%Implementer denne i Solution.m.
'''
new_solution = new_solution.tabu_search_heuristic(containers, 4000)
new_solution.calculate_objective(containers)
new_solution.print_sol()
print(new_solution.objective)




