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
        for (u, v) in E
            d[v] = ω[(u, v)]
            father[v] = u
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
    
    return "There is no positive weight cycle in G"
end
