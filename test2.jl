using LightGraphs, JuMP, Gurobi, JSON

# Positive Weight Cycle Detection
function positive_weight_cycle_detection(G, ω)
    V = vertices(G)
    E = edges(G)
    n = length(V)
    d = zeros(n)
    father = zeros(Int, n)
    C = []
    
    for i in 1:n
        d[i] = Inf
    end
    
    for (u, v) in V × V
        d[u] = 0
        for v in V
            d[v] = 0
            for (u, v) in E
                d[u] = -ω[(u, v)]
                father[u] = v
            end
        end
        
        for w in V
            for (u, v) in V × V
                if d[u] > d[w] + ω[(w, v)]
                    d[u] = d[w] + ω[(w, v)]
                    father[u] = father[v]
                    
                    if u == v && d[u] < 0
                        while true
                            w = father[u]
                            push!(C, (w, v))
                            v = w
                            if v == u
                                break
                            end
                        end
                        return C
                    end
                end
            end
        end
    end
    
    return "There is no positive weight cycle in G"
end

# Construct the graph from compatibility table
function construct_graph(compatibilities)
    V = Set{Any}()
    E = Set{Tuple{Any, Any}}()
    ω = Dict{Tuple{Any, Any}, Float64}()

    for (d, p) in keys(compatibilities)
        push!(V, d)
        push!(V, p)
        push!(E, (d, p))
        ω[(d, p)] = -compatibilities[(d, p)]
    end

    return V, E, ω
end

# Solve positive weight cycle detection problem
function solve_positive_weight_cycle_detection(compatibilities)
    V, E, ω = construct_graph(compatibilities)
    G = SimpleGraph(V, collect(E))  # Pass the set of edges as an array
    C = positive_weight_cycle_detection(G, ω)
    return C
end

# Test the code with the compatibility table
compatibilities = Dict{Any, Float64}(
    (1, 1) => 0.5,
    (1, 2) => 0.6, (1, 3) => 0.0, (1, 4) => 0.0, (1, 5) => 0.0, (1, 6) => 0.0,
    (2, 1) => 0.8,
    (2, 2) => 0.4, (2, 3) => 0.0, (2, 4) => 0.0, (2, 5) => 0.0, (2, 6) => 0.0,
    (3, 1) => 0.0, (3, 2) => 0.0, (3, 3) => 0.0,
    (3, 4) => 0.4, (3, 5) => 0.0, (3, 6) => 0.0,
    (4, 1) => 0.0, (4, 2) => 0.0,
    (4, 3) => 0.5, (4, 4) => 0.0,
    (4, 5) => 0.5, (4, 6) => 0.0,
    (5, 1) => 0.0, (5, 2) => 0.0,
    (5, 3) => 0.7, (5, 4) => 0.0, (5, 5) => 0.0, (5, 6) => 0.0,
    (6, 1) => 0.0, (6, 2) => 0.0, (6, 3) => 0.0, (6, 4) => 0.0,
    (6, 5) => 0.9,
    (6, 6) => 0.8
)

C = solve_positive_weight_cycle_detection(compatibilities)

# Print the positive weight cycle if found
if isa(C, Array)
    println("Positive Weight Cycle:")
    for (u, v) in C
        println("($u, $v)")
    end
else
    println(C)
end
