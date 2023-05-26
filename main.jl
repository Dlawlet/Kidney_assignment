using JuMP
using Gurobi

function positive_weight_cycle_detection(G, ω)
    V = 1:size(G)[1]
    E = [(u, v) for u in V, v in V if G[u, v] == 1] # set of edges

    model = Model(optimizer_with_attributes(Gurobi.Optimizer, "OutputFlag" => 0))

    @variable(model, d[u in V] >= 0)   # Distance variables
    @variable(model, f[u in V, v in V] >=0 )   # Indicator variables for edges in the cycle

    # Objective: Minimize the total distance
    @objective(model, Min, sum(d[u] for u in V))

    # Constraints: Distance update
    for u in V
        for v in V
            @constraint(model, d[u] <= d[v] + ω[u, v])
        end
    end

    # Constraints: Flow conservation
    for u in V
        @constraint(model, sum(f[u, v] for v in V) - sum(f[v, u] for v in V) == 0)
    end

    # Constraint: Positive weight cycle
    @constraint(model, sum(ω[u, v] * f[u, v] for (u, v) in E) >= 1e-6)

    optimize!(model)

    if termination_status(model) == MOI.OPTIMAL
        cycle = []
        for (u, v) in E
            println("f[$u, $v] = ", value(f[u, v]))
            if value(f[u, v]) > 0
                push!(cycle, (u, v))
            end
        end
        return cycle
    else
        return []
    end
end

# Test

G = ([0 1 0 0 0 0;
     1 0 0 0 0 0;
     0 0 0 1 0 0;
     0 0 1 0 1 0;
     0 0 1 0 0 0;
     0 0 0 0 1 0])

ω = ([0.5 0.6 0 0 0 0;
     0.8 0.4 0 0 0 0;
     0 0 0 0.4 0 0;
     0 0 0.5 0 0.5 0;
     0 0 0.7 0 0 0;
     0 0 0 0 0.9 0.8])
# Call the positive_weight_cycle_detection function
cycle = positive_weight_cycle_detection(G, ω)

# Check if a positive weight cycle was found
if isempty(cycle)
    println("No positive weight cycle found.")
else
    println("Positive weight cycle found:")
    println(cycle)
end
