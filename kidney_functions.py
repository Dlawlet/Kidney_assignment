import gurobipy as gp
from gurobipy import GRB
import csv
from copy import deepcopy

def convert_to_tuples(lst):
    if len(lst) < 2:
        return [(lst[0], lst[0])]
    
    result = [(lst[i], lst[i+1]) for i in range(len(lst) - 1)]
    if lst[-1] == lst[0]:
        result.append((lst[-1], lst[0]))
    if result[-1][0] == result[-1][1]:
        result.pop()
    return result

def kydneys(donors, patients, weights, M, C, nb_pairs ):

    # Create a new model
    model = gp.Model("KidneyExchange")

    # Create decision variables
    x = model.addVars(donors, patients, vtype=GRB.BINARY, name="x") #meaning x[d, p] = 1 if donor d is assigned to patient p, 0 otherwise

    # complete x with 0s
    for d in range(nb_pairs):
        for p in range(nb_pairs):
            if (d, p) not in weights:
                x[d, p] = model.addVar(vtype=GRB.BINARY, name=f"x[{d},{p}]")
                weights[(d, p)] = 0
                x[d, p].start = 0
    # Set objective function
    obj = gp.quicksum(weights[d, p] * x[d, p] for d, p in weights)
    model.setObjective(obj, GRB.MAXIMIZE)

    
    
    for d in donors:
        model.addConstr(gp.quicksum(x[d, p] for p in patients) <= 1)

    # Add assignment constraints (each patient can receive at most one donor)
    for p in patients:
        model.addConstr(gp.quicksum(x[d, p] for d in donors) <= 1)

    # Add constraints ∑(u,v)∈c x[u][v] ⩽ |c| − 1 for each cycle c in C to avoid cycles performing strictly more than M exchanges
    #print(x)
    for cycle in C:
        cycle = convert_to_tuples(cycle)
        model.addConstr(gp.quicksum(x[int(u), int(v)] for u, v in cycle) <= len(cycle) - 1)
    

    # Optimize the model
    model.setParam("OutputFlag", 0)
    model.optimize()
    solution = []
    # Print the optimal solution
    if model.status == GRB.OPTIMAL:
        for d in donors:
            for p in patients:
                if x[d, p].x > 0:
                    solution.append((str(d), str(p)))
    else:
        print("No solution found.")
    return solution, model.objVal


def form_chain_and_cycles(edges):
    chains = []
    cycles = []
    nodes = set()
    
    # Create a dictionary to store the edges
    edge_dict = {}
    for edge in edges:
        giver, receiver = edge
        edge_dict[giver] = receiver
        nodes.add(giver)
        nodes.add(receiver)
    
    # Find the starting nodes for the chains
    start_nodes = nodes.difference(edge_dict.values())
    
    # Traverse the edges to form the chains
    for start_node in start_nodes:
        chain = []
        current_node = start_node
        while current_node is not None:
            chain.append(current_node)
            current_node = edge_dict.get(current_node)
        chains.append(chain)
    
    # Find cycles in the edges
    visited = set()
    for node in nodes:
        if node not in visited:
            cycle = find_cycle(node, [], edge_dict, visited)
            if cycle:
                cycle.append(cycle[0])
                cycles.append(cycle)
    final = []
    for chain in chains:
        final.append(chain)
    for cycle in cycles:
        final.append(cycle)
    return final

def find_disjoint_cycles(graph):
    cycles = []

    while graph:
        cycle = []
        start_node = next(iter(graph))
        current_node = start_node

        while True:
            cycle.append(current_node)
            next_node = ""
            if current_node in graph:
                next_node = graph[current_node][0]
            else:
                break

            del graph[current_node]

            if next_node == start_node:
                cycle.append(next_node)
                break

            current_node = next_node

        cycles.append(cycle)

    return cycles

def find_cycle(node, path, edge_dict, visited):
    if node in path:
        cycle_start = path.index(node)
        return path[cycle_start:]
    
    visited.add(node)
    path.append(node)
    next_node = edge_dict.get(node)
    if next_node:
        return find_cycle(next_node, path, edge_dict, visited)
    
    return None
