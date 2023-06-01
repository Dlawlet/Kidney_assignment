import networkx as nx
import gurobipy as gp


def positive_weight_cycle_detection(graph, edgeweights):
    V = graph.nodes()
    E = graph.edges()

    # Create a Gurobi model
    model = gp.Model()
    #Gurobi environment GRB 

    # Variables
    duv = {}
    fatheruv = {}

    for u in V:
        for v in V:
            GRB = gp.GRB
            duv[u, v] = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name=f"duv{u}{v}")
            fatheruv[u, v] = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name=f"fatheruv{u}_{v}")

    model.update()

    # Objective function (not required for positive weight cycle detection)

    # Constraints
    for u in V:
        for v in V:
            expr = gp.LinExpr()
            expr.addTerms(1, duv[u, v])
            expr.addTerms(-1, duv[u, v])
            model.addConstr(expr, GRB.EQUAL, 0, name=f"duv{u}{v} = 0")

    # Update the model to integrate changes
    model.update()

    # Set objective sense to minimize (not required for positive weight cycle detection)
    model.setObjective(0, GRB.MAXIMIZE)


    # Optimize the model
    model.optimize()

    # Extract positive weight cycles
    cycles = set()
    for u in V:
        for v in V:
            if duv[u, v].x < 0:
                w = fatheruv[u, v].x
                cycle = [(w, v)]
                while v != u:
                    v = w
                    w = fatheruv[u, v].x
                    cycle.append((w, v))
                cycles.add(tuple(cycle))

    if cycles:
        return cycles
    else:
        return None
    
compatibilities = {
    ('d1', 'p1'): 0.5,
    ('d1', 'p2'): 0.6,
    ('d2', 'p1'): 0.8,
    ('d2', 'p2'): 0.4,
    ('d3', 'p4'): 0.4,
    ('d4', 'p3'): 0.5,
    ('d4', 'p5'): 0.5,
    ('d5', 'p3'): 0.7,
    ('d6', 'p5'): 0.9,
    ('d6', 'p6'): 0.8
}
G = nx.DiGraph()
G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_edges_from([(1,1),(1,2),(2,1),(2,2),(2,3),(3,4),(4,3),(4,5),(5,3),(6,5),(6,6)])
edgeweights = {(1, 2): 0.5,(1,2): 0.6,(2,1):0.8, (2,2):0.4, (3,4):0.4, (4,3):0.5, (4,5):0.5, (5,3):0.7, (6,5):0.9, (6,6):0.8}
print(positive_weight_cycle_detection(G, edgeweights))