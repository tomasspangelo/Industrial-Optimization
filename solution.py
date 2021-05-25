import numpy as np
import copy
from container import Container


class Solution:
    """
    Object that represents a solution with appropriate methods for
    permuting the solution.
    """

    def __init__(self, bay, stack, tier):
        """
        Constructor.
        """
        self.flowX = np.zeros((bay, stack, tier))
        self.objective = 2.2e-200
        self.cog = [2.2e-200, 2.2e-200]
        self.total_weight_containers = 2.2e-200

    def make_copy(self):
        """
        Makes a copy of the solution.
        """
        return copy.deepcopy(self)

    def construct(self):
        """
        Simple construction heuristic.
        Takes the first container in the list, and places it in the
        first location. The next is placed in the second location and
        so on.
        """
        nBays = self.flowX.shape[0]
        nStacks = self.flowX.shape[1]
        nTiers = self.flowX.shape[2]
        i = 1
        for b in range(nBays):
            for s in range(nStacks):
                for t in range(nTiers):
                    self.flowX[b, s, t] = i
                    i += 1

    def calculate_objective(self, containers):
        """
        Calculates and updates the objective value for the Solution object.
        """
        nBays = self.flowX.shape[0]
        nStacks = self.flowX.shape[1]
        nTiers = self.flowX.shape[2]

        gravity_goal = [nBays / 2, nStacks / 2]

        gravity_this = [0, 0]

        sum_container_weight = 0
        for b in range(nBays):
            for s in range(nStacks):
                sum_tier = 0
                for t in range(nTiers):
                    sum_tier += containers[self.flowX[b, s, t]].weight
                    sum_container_weight += containers[self.flowX[b, s, t]].weight
                gravity_this[0] += (b + 1 - 0.5) * sum_tier
                gravity_this[1] += (s + 1 - 0.5) * sum_tier

        gravity_this[0] /= sum_container_weight
        gravity_this[1] /= sum_container_weight
        evaluation = (gravity_goal[0] - gravity_this[0]) ** 2 + (gravity_goal[1] - gravity_this[1]) ** 2
        self.objective = evaluation
        self.cog = gravity_this
        self.total_weight_containers = sum_container_weight

        return self.objective

    def print_sol(self):
        """
        Method for printing the solution.
        """
        nBays = self.flowX.shape[0]
        nStacks = self.flowX.shape[1]
        nTiers = self.flowX.shape[2]
        print("Current solution:")
        for b in range(nBays):
            for s in range(nStacks):
                for t in range(nTiers):
                    x = {
                        'b': b,
                        's': s,
                        't': t,
                        'container': self.flowX[b, s, t]
                    }
                    print(x)

    def construction_improved(self, containers):
        """
        Improved construction heuristic. Uses domain knowledge to strategically
        place the containers according to position and weight. The heuristic
        tries to do this whilst balancing weight along opposite sides of the vessel.

        """
        nBays = self.flowX.shape[0]
        nStacks = self.flowX.shape[1]
        nTiers = self.flowX.shape[2]

        descending = Container.sort_array_weight_descending(containers)
        ascending = Container.sort_array_weight_ascending(containers)

        # Start with filling the most heavy containers in the middle
        middle_bay = [int(nBays / 2)] if nBays % 2 != 0 else [int((nBays / 2) - 1), int(nBays / 2)]
        middle_stack = [int(nStacks / 2)] if nStacks % 2 != 0 else [int((nStacks / 2) - 1), int(nStacks / 2)]
        i = 0

        for t in range(nTiers):
            if len(middle_bay) == 2 and len(middle_stack) == 2 and len(descending[i:]) >= 4:
                cont1 = descending[i]
                cont2 = descending[i + 1]
                cont3 = descending[i + 2]
                cont4 = descending[i + 3]
                rand = np.random.uniform()
                self.flowX[middle_bay[0], middle_stack[0], t] = cont1 if rand < 0.5 else cont2
                self.flowX[middle_bay[0], middle_stack[1], t] = cont3 if rand < 0.5 else cont4
                self.flowX[middle_bay[1], middle_stack[0], t] = cont4 if rand < 0.5 else cont3
                self.flowX[middle_bay[1], middle_stack[1], t] = cont2 if rand < 0.5 else cont1
                i += 4
            elif len(middle_bay) == 2 and len(middle_stack) == 1 and len(descending[i:]) >= 2:
                cont1 = descending[i]
                cont2 = descending[i + 1]
                conts = np.array([cont1, cont2])
                np.random.shuffle(conts)
                self.flowX[middle_bay[0], middle_stack[0], t] = conts[0]
                self.flowX[middle_bay[1], middle_stack[0], t] = conts[1]
                i += 2
            elif len(middle_bay) == 1 and len(middle_stack) == 2 and len(descending[i:]) >= 2:
                cont1 = descending[i]
                cont2 = descending[i + 1]
                rand = np.random.uniform()
                self.flowX[middle_bay[0], middle_stack[0], t] = cont1 if rand < 0.5 else cont2
                self.flowX[middle_bay[0], middle_stack[1], t] = cont2 if rand < 0.5 else cont1
                i += 2
            elif len(middle_bay) == 1 and len(middle_stack) == 1 and len(descending[i:]) >= 1:
                self.flowX[middle_bay[0], middle_stack[0], t] = descending[i]
                i += 1

        # Fill the most light containers around the "bay" edges
        i = 0
        for b in range(int(nBays / 2)):
            for t in range(nTiers):
                cont1 = ascending[i]
                cont2 = ascending[i + 1]
                cont3 = ascending[i + 2]
                cont4 = ascending[i + 3]
                conts = np.array([cont1, cont2, cont3, cont4])
                np.random.shuffle(conts)
                if conts[0] not in self.flowX and conts[1] not in self.flowX:
                    if self.flowX[b, 0, t] == 0:
                        self.flowX[b, 0, t] = conts[0]
                    if self.flowX[b, nStacks - 1, t] == 0:
                        self.flowX[b, nStacks - 1, t] = conts[1]
                if conts[2] not in self.flowX and conts[3] not in self.flowX:
                    if self.flowX[nBays - 1 - b, 0, t] == 0:
                        self.flowX[nBays - 1 - b, 0, t] = conts[2]
                    if self.flowX[nBays - 1 - b, nStacks - 1, t] == 0:
                        self.flowX[nBays - 1 - b, nStacks - 1, t] = conts[3]
                i += 4

        # Fill the most light containers around the "stack" edges
        for s in range(1, int(nStacks / 2) + 1):
            for t in range(nTiers):
                cont1 = ascending[i]
                cont2 = ascending[i + 1]
                conts = np.array([cont1, cont2])
                np.random.shuffle(conts)
                if conts[0] not in self.flowX and conts[1] not in self.flowX:
                    if self.flowX[0, s, t] == 0:
                        self.flowX[0, s, t] = conts[0]
                    if self.flowX[nBays - 1, nStacks - 1 - s, t] == 0:
                        self.flowX[nBays - 1, nStacks - 1 - s, t] = conts[1]

        # Fill the remaining randomly
        zero_cells = np.where(self.flowX == 0)
        asc_copy = np.copy(ascending)
        np.random.shuffle(asc_copy)
        i = 0
        for j in range(len(zero_cells[0])):
            cont = asc_copy[i]
            while True:
                if cont in self.flowX:
                    i += 1
                    cont = asc_copy[i]
                else:
                    break
            self.flowX[zero_cells[0][j], zero_cells[1][j], zero_cells[2][j]] = cont

    def local_search_two_swap(self, containers):
        """
        2-container swap local search.
        """
        obj_val = self.calculate_objective(containers)
        sol = self.make_copy()

        improved = True
        best = None
        while improved:
            improved = False
            for i in range(1, len(containers) + 1):
                for j in range(i + 1, len(containers) + 1):
                    cont1 = np.where(sol.flowX == containers[i].id)
                    cont2 = np.where(sol.flowX == containers[j].id)
                    sol.flowX[cont1[0][0], cont1[1][0], cont1[2][0]] = containers[j].id
                    sol.flowX[cont2[0][0], cont2[1][0], cont2[2][0]] = containers[i].id
                    new_obj_val = sol.calculate_objective(containers)
                    if new_obj_val < obj_val:
                        obj_val = sol.calculate_objective(containers)
                        best = np.copy(sol.flowX)
                        improved = True
                    sol = self.make_copy()
            self.flowX = best if improved else self.flowX
            obj_val = self.calculate_objective(containers)
            sol = self.make_copy()

    def local_search_three_swap(self, containers):
        """
        3-container swap local search
        """
        obj_val = self.calculate_objective(containers)
        sol = self.make_copy()

        improved = True
        best = None
        while improved:
            improved = False
            for i in range(1, len(containers) + 1):
                for j in range(i + 1, len(containers) + 1):
                    for k in range(j + 1, len(containers) + 1):
                        perturbations = [[j, k, i], [k, i, j]]
                        for p in perturbations:
                            cont1 = np.where(sol.flowX == containers[i].id)
                            cont2 = np.where(sol.flowX == containers[j].id)
                            cont3 = np.where(sol.flowX == containers[k].id)
                            sol.flowX[cont1[0][0], cont1[1][0], cont1[2][0]] = containers[p[0]].id
                            sol.flowX[cont2[0][0], cont2[1][0], cont2[2][0]] = containers[p[1]].id
                            sol.flowX[cont3[0][0], cont3[1][0], cont3[2][0]] = containers[p[2]].id
                            new_obj_val = sol.calculate_objective(containers)
                            if new_obj_val < obj_val:
                                obj_val = sol.calculate_objective(containers)
                                best = np.copy(sol.flowX)
                                improved = True
                            sol = self.make_copy()
            self.flowX = best if improved else self.flowX
            obj_val = self.calculate_objective(containers)
            sol = self.make_copy()

    def two_swap_neighborhood(self, containers):
        """
        Method for generating the neighborhood/candidate list given
        the current solution (self).
        """
        obj_val = self.calculate_objective(containers)
        sol = self.make_copy()

        candidates = []
        for i in range(1, len(containers) + 1):
            for j in range(i + 1, len(containers) + 1):
                cont1 = np.where(sol.flowX == containers[i].id)
                cont2 = np.where(sol.flowX == containers[j].id)
                # To explore more of the solution space, it is prohibited to
                # swap within a stack.
                if cont1[0][0] == cont2[0][0] and cont1[1][0] == cont2[1][0]:
                    continue

                sol.flowX[cont1[0][0], cont1[1][0], cont1[2][0]] = containers[j].id
                sol.flowX[cont2[0][0], cont2[1][0], cont2[2][0]] = containers[i].id
                sol.calculate_objective(containers)

                obj_val = sol.calculate_objective(containers)
                candidates.append((i, j, obj_val))
                sol = self.make_copy()

        return sorted(candidates, key=lambda x: x[2], reverse=False)

    def tabu_search_heuristic(self, containers, iter, n=100):
        """
        Tabu search heuristic based on the two-container swap local search
        """
        current = self.make_copy()
        tabu_list = {
            1: [],
            2: [],
            3: [],
        }

        i = 0
        while i < iter:
            i += 1

            # Every n iteration, do a random perturbation to diversify the search
            if i % n == 0:
                choices = [c for c in containers]
                choices = np.random.choice(choices, size=3, replace=False)
                perturbations = [[choices[1], choices[2], choices[0]],
                                 [choices[2], choices[0], choices[1]]]
                r = np.random.choice([0, 1], size=None, replace=False)
                p = perturbations[r]
                cont1 = np.where(current.flowX == choices[0])
                cont2 = np.where(current.flowX == choices[1])
                cont3 = np.where(current.flowX == choices[2])
                current.flowX[cont1[0][0], cont1[1][0], cont1[2][0]] = containers[p[0]].id
                current.flowX[cont2[0][0], cont2[1][0], cont2[2][0]] = containers[p[1]].id
                current.flowX[cont3[0][0], cont3[1][0], cont3[2][0]] = containers[p[2]].id
                continue

            candidate_list = current.two_swap_neighborhood(containers)
            add_tabu = None
            for j in range(len(candidate_list)):
                tabu_members = []
                for key in tabu_list:
                    tabu_members += tabu_list[key]

                k = candidate_list[j][0]
                l = candidate_list[j][1]
                if k not in tabu_members and l not in tabu_members:
                    cont1 = np.where(current.flowX == containers[k].id)
                    cont2 = np.where(current.flowX == containers[l].id)
                    current.flowX[cont1[0][0], cont1[1][0], cont1[2][0]] = containers[l].id
                    current.flowX[cont2[0][0], cont2[1][0], cont2[2][0]] = containers[k].id
                    add_tabu = [k, l]
                    break

            for j in range(3, 1, -1):
                tabu_list[j] = tabu_list[j - 1]
            tabu_list[1] = add_tabu
        return current
