CODE_FOR_BUILD = """BUILD-HEAP(A[1,...,n]) {
    for i = floor(n/2) downto 1
        HeapifyDown(A, i)
}
"""

CODE_FOR_EXTRACT = """EXTRACT-FIRST(A) {
    heapsize = length(A)
    Exchange A[1] with A[heapsize]
    Remove A[heapsize]
    HeapifyDown(A, 1)
}
"""

CODE_FOR_INSERT = """INSERT(A, value) {
    heapsize = length(A) + 1
    A[heapsize] = value
    HeapifyUp(A, heapsize)
}
"""

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
    curr_level, next_level = ∅, ∅
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
    Edges = ∅
    ReachSet = ∅
    UnReachSet = G.V
    add an arbitrary vertex v to ReachSet
    while ReachSet ≠ G.V
        find (v, u) be the min edge such that
        v ∈ ReachSet and u ∈ UnReachSet
        Edges = Edges ∪ {(v, u)}
        ReachSet = ReachSet ∪ {u}
        UnReachSet = UnReachSet - {u}
    return Edges
}
"""

CODE_FOR_PRIM_QUEUE = """MST-PRIM(G) {
    Edges = ∅
    UnReachSet = G.V
    set all vertices v.minEdge = ∅
    set all vertices v.key = ∞
    set an arbitrary vertex v.key = 0
    while UnReachSet ≠ ∅
        v = EXTRACT-MIN(UnReachSet)
        if v.minEdge ≠ ∅
            add v.minEdge to Edges
        for each neighbor u of v
            if u ∈ UnReachSet and
            weight(v, u) < u.key
                u.key = weight(v, u)
                u.minEdge = (v, u)
    return Edges
}
"""


CODE_FOR_KRUSKAL = """MST-KRUSKAL(G) {
    Edges = ∅
    scan all edges by nondecreasing weight
        if an edge is safe (does not form
        any cycle with the MST so far)
            add the edge to Edges
    return Edges 
}
"""

CODE_FOR_KRUSKAL_CHINESE = """MST-KRUSKAL(G) {
    Edges = ∅
    按从小到大的顺序检查每条边
        如果这条边是安全的（没有和最小生成树形成任何环）
            将这条边加入 Edges
    return Edges 
}
"""


CODE_FOR_KRUSKAL_UNION_FIND = """MST-KRUSKAL(G) {
    Edges = ∅
    for each vertex v ∈ G.V
        MAKE-SET(v)
    scan all edges by nondecreasing weight
    for each edge (u, v)
        if FIND-SET(u) ≠ FIND-SET(v)
            Edges = Edges ∪ {(u, v)}   
            UNION(u, v)
    return Edges 
}
"""

CODE_FOR_DIJKASTRA_WITH_RELAX = """DIJKSTRA(G, s) {
    UnReachSet = G.V
    set all vertices v.minEdge = ∅
    set all vertices v.key = ∞
    set an arbitrary vertex v.key = 0
    while UnReachSet ≠ ∅
        v = EXTRACT-MIN(UnReachSet)
        for each neighbor u of v
            RELAX(u, v, G.Weight)
}
}
"""

CODE_FOR_RELAX = """RELAX(u, v, weight) {
    if v.key > u.key + weight(u, v)
        v.key = u.key + weight(u, v)
        v.previous = u
}
"""

CODE_FOR_DIJKASTRA_WITHOUT_RELAX = """DIJKSTRA(G, s) {
    UnReachSet = G.V
    set all vertices v.key = ∞
    set all vertices v.previous = ∅
    s.key = 0
    while UnReachSet ≠ ∅
        v = EXTRACT-MIN(UnReachSet)
        for each neighbor u of v
            // Relax edge (v, u)
            if u.key > v.key + weight(u, v)
                u.key = v.key + weight(u, v)
                u.previous = v
}
"""

CODE_FOR_DIJKASTRA_WITHOUT_RELAX_CH = """DIJKSTRA(G, s) {
    UnReachSet = G.V
    对于每一个点v设置 v.key = ∞
    对于每一个点v设置 v.previous = ∅
    对于源点s设置 s.key = 0
    while UnReachSet ≠ ∅
        v = EXTRACT-MIN(UnReachSet)
        对于从v出发的每条边(v, u)
            // 松弛边(v, u)
            if u.key > v.key + weight(u, v)
                u.key = v.key + weight(u, v)
                u.previous = v
}
"""

CODE_FOR_BELLMAN_FORD = """BELLMAN-FORD(G, s) {
    UnReachSet = G.V
    set all vertices v.key = ∞
    set all vertices v.previous = ∅
    s.key = 0
    for i = 1 to |G.V| - 1
        for each edge (v, u)
            // Relax edge (v, u)
            if u.key > v.key + weight(u, v)
                u.key = v.key + weight(u, v)
                u.previous = v
    // Check negative cycle
    for each edge (v, u)
        if u.key > v.key + weight(u, v)
            return FALSE
    return True
}
"""