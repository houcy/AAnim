CODE_FOR_DFS = """DFS(G) {
    for each vertex u
        if u.color = BLACK
            DFS-VISIT(G, u)
}

DFS-VISIT(G, u) {
    u.color = PINK
    for each neighbor v of u
        if v.color = BLACK
            DFS-VISIT(G, v)
    u.color = BLUE
}
"""

CODE_FOR_BFS = """BFS(G, s) {
    s.color = PINK
    Q = ∅
    ENQUEUE(Q, s)
    while Q != ∅
        u = DEQUEUE(Q)
        u.color = PINK
        for each neighbor v of u
            if v.color = BLACK
                v.color = WHITE
                ENQUEUE(Q, v)
        u.color = BLUE
}
"""

CODE2_FOR_BFS = """BFS(G, s) {
    curr_level = ∅
    next_level = ∅
    ENQUEUE(curr_level, s)
    s.color = PINK
    while curr_level != ∅
        for each u in curr_level:
            for each neighbor v of u
                if v.color = BLACK
                    ENQUEUE(next_level, v)
                    v.color = WHITE
        u.color = BLUE
        curr_level = next_level
        mark PINK for all v in curr_level
        next_level = ∅
}
"""

CODE_FOR_PRIM_BASIC = """MST-PRIM(G) {
    T = ∅;
    add an arbitrary v vertex to U;
    while (U ≠ V)
        find (u, v) be the min edge
        such that u ∈ V - U
        T = T ∪ {(u, v)}
        U = U ∪ {v}
}
"""

CODE_FOR_PRIM_QUEUE = """MST-PRIM(G, w, s) {
    for each vertex v
        v.key = ∞
    s.key = 0
    Q = G.V
    T = Φ
    while Q != Φ
        v = EXTRACT-MIN(Q)
        add edge(v) to T
        for each neighbor u of v
            if u ∈ Q and w(u, v) < u.key
                edge(u) = uv
                u.key = w(u, v)
}
"""