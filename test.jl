function positive_weight_cycle_detection(G, W)
    Cycle = []
    V = 1:size(G, 1) # set of vertices
    E = [(u, v) for u in V, v in V if G[u, v] == 1] # set of edges

    # distance matrix of size |V| x |V|
    d = fill(Inf, size(G))

    father = fill(0, size(G))

    for v in V
        d[v, v] = 0
    end
    for (u, v) in E
        d[u, v] = W[u, v]
        d[v, u] = -W[u, v]  # Reverse direction with negated weight
        father[u, v] = u
        father[v, u] = v  # Reverse direction
    end

    for w in V
        for u in V
            for v in V
                if d[u, v] > d[u, w] + d[w, v]
                    d[u, v] = d[u, w] + d[w, v]
                    father[u, v] = father[w, v]
                end
                if u == v && d[u, u] < 0
                    w = father[u, v]
                    push!(Cycle, (w, v))
                    v = w
                    while v != u
                        w = father[u, v]
                        push!(Cycle, (w, v))
                        v = w
                    end
                    return Cycle    
                end
                
            end
        end
    end

    return Cycle
end

# Test

G = transpose([0 1 0 0 0 0;
     1 0 0 0 0 0;
     0 0 0 1 0 0;
     0 0 1 0 1 0;
     0 0 1 0 0 0;
     0 0 0 0 1 0])

ω = transpose([0.5 0.6 0 0 0 0;
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
