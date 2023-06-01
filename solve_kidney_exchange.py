from kidney_functions import *

def solve_kidney_exchange(filename, solve_cycles=False):
    # Read data from the CSV file
    head = True
    weights = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if head:
                head = False
                nb_pairs = int(row[0])
                nb_links = int(row[1])
                M = int(row[2])
                continue
            weights[(int(row[0])), (int(row[1]))] = float(row[2])

    # Create sets of donors and patients
    donors = set()
    patients = set()
    for d, p in weights:
        donors.add(d)
        patients.add(p)

    if solve_cycles:

        print("Start solving for kidney exchange with cycle")
        print(f"Size of donors: {len(donors)}, size of patients: {len(patients)}")

        copy_weights = deepcopy(weights)
        copy_donors = deepcopy(donors)
        copy_patients = deepcopy(patients)
        C = []  # list of cycles

        while True:
            inside = False
            solution = kydneys(copy_donors, copy_patients, copy_weights, M, C, nb_pairs)
            # Check solution's cycles exceed the maximum cycle length
            for cycle in form_chain_and_cycles(solution):
                if len(cycle) - 1 > M:
                    C.append(cycle)
                    inside = True
                    copy_weights = deepcopy(weights)
                    copy_donors = deepcopy(donors)
                    copy_patients = deepcopy(patients)
            if not inside:
                break

        print("enf of solving for kidney exchange with cycle")
        print()
        print(f"Optimal solution depends on cycle length {M}")
        print(solution)
        print()
        
        for d, p in solution:

            print(f"Assign donor {d} to patient {p}")
        print("Cycles of the solution:", form_chain_and_cycles(solution))

        init_graph = {} 
        for d, p in solution:
                if d not in init_graph:
                    init_graph['d' + str(d)] = ['p' + str(p)]
                    init_graph['p' + str(p)] = ['d' + str(p)]
                else:
                    init_graph['d' + str(d)].append('p' + str(p))
                    init_graph['p' + str(p)].append('d' + str(p))
        return weights, init_graph

    else :

        print("Start solving for kidney exchange")

        # Create a new optimization model
        model = gp.Model("KidneyExchange")

        # Create decision variables
        x = model.addVars(donors, patients, vtype=GRB.BINARY, name="x")

        # Complete the decision variable matrix with 0s for missing entries
        for d in range(nb_pairs):
            for p in range(nb_pairs):
                if (d, p) not in weights:
                    x[d, p] = model.addVar(vtype=GRB.BINARY, name=f"x[{d},{p}]")
                    weights[(d, p)] = 0
                    x[d, p].start = 0

        # Set the objective function
        obj = gp.quicksum(weights[d, p] * x[d, p] for d, p in weights)
        model.setObjective(obj, GRB.MAXIMIZE)

        for d in donors:
            model.addConstr(gp.quicksum(x[d, p] for p in patients) <= 1)
        for p in patients:
            model.addConstr(gp.quicksum(x[d, p] for d in donors) <= 1)

        # Optimize the model
        model.setParam("OutputFlag", 0)
        model.optimize()

        # Print the optimal solution
        if model.status == GRB.OPTIMAL:

            print(f"Size of donors: {len(donors)}, size of patients: {len(patients)}")
            print("enf of solving for kidney exchange with cycle")
            print("Optimal solution:")

            for d in donors:
                for p in patients:
                    if x[d, p].x > 0:
                        print(f"Assign donor {d} to patient {p}")
        
            init_graph = {} 
            for d in donors:
                for p in patients:
                    if x[d, p].x > 0:
                        if d not in init_graph:
                            init_graph['d' + str(d)] = ['p' + str(p)]
                            init_graph['p' + str(p)] = ['d' + str(p)]
                        else:
                            init_graph['d' + str(d)].append('p' + str(p))
                            init_graph['p' + str(p)].append('d' + str(p))
            return weights, init_graph
