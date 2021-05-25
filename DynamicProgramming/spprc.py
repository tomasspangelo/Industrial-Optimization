"""
Main algorithm for shortest path problems with resource constraint (Dynamic Programming)
"""

from utils import read_data
import time
import numpy as np
from resource import resource
from dominate import dominate

# Load data, initialize variables
nNodes, wTime, wInco, Network = read_data("./Network3.m")
Network = np.array(Network)
pair = (18, 25)
label = {
    'Cost': 0,
    'Time': 0,
    'Inco': 0,
    'Path': [1],
    'Pair': 0,
    'Visit': [0 for _ in range(nNodes)],
    'Done': False,
}
new_label = label.copy()
new_label['Visit'][0] = 1
new_label['Pair'] = 1 if 1 == pair[0] else 0
new_label['Pair'] = -1 if 1 == pair[1] else new_label['Pair']
l = [new_label]
it = -1
num_dominated = 0

# Main loop
start_time = time.perf_counter()
while it + 1 < len(l):
    it = it + 1
    if not l[it]['Done']:
        for i in range(len(Network)):
            if Network[i, 0] == l[it]['Path'][-1]:
                new_label = l[it].copy()
                new_label['Path'] = l[it]['Path'].copy()
                new_label['Visit'] = l[it]['Visit'].copy()
                new_label['Cost'] += Network[i, 2]
                new_label['Time'] += Network[i, 3]
                new_label['Inco'] += Network[i, 4]
                new_label['Path'].append(Network[i, 1])
                new_label['Visit'][Network[i, 1] - 1] += 1
                if Network[i, 1] == pair[0]:
                    new_label['Pair'] += 1
                elif Network[i, 1] == pair[1]:
                    new_label['Pair'] -= 1
                if resource(new_label, wTime, wInco):
                    l.append(new_label)
                    dominated = dominate(l)
                    num_dominated += len(dominated)
                    '''
                    for j in range(len(dominated)):
                        l[dominated[j]]["Done"] = True
                    '''
    l[it]["Done"] = True

# Problem solved, print solution
end_time = time.perf_counter()
output = 'Number of labels created: ' + str(len(l))
print(output)
output = 'Number of labels dominated : ' + str(num_dominated)
print(output)
output = 'The algorithm took : ' + str(end_time - start_time) + ' seconds';
print(output)

# Find the best label
best_label = dict(label)
best_label['Cost'] = float('inf')
for i in range(1, len(l)):
    if l[i]["Path"][-1] == nNodes and l[i]["Cost"] < best_label['Cost'] and l[i]['Pair'] == 0:
        best_label = l[i]

print("Best label:")
print(best_label)
