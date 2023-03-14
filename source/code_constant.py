CODE_FOR_BUILD = """BUILD_HEAP(A[1,...,n]) {
    for i = floor(n/2) downto 1
        HeapifyDown(A, i)
}
"""

CODE_FOR_EXTRACT = """EXTRACT_FIRST(A) {
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

CODE_FOR_DFS = """DFS(Graph) {
    for each vertex u
        if u.color = BLACK
            DFS_VISIT(G, u)
}

DFS_VISIT(Graph, u) {
    u.color = PINK
    for each neighbor v of u
        if v.color = BLACK
            DFS_VISIT(G, v)
    u.color = BLUE
}
"""

CODE_FOR_BFS = """BFS(Graph, source) {
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

CODE2_FOR_BFS = """BFS(Graph, source) {
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

CODE_FOR_PRIM_BASIC = """PRIM_IDEA(Graph) {
    Edges = ∅
    ReachSet = ∅
    UnReachSet = G.V
    add an arbitrary vertex v to ReachSet
    while ReachSet ≠ G.V
        find (u, v) be the min edge such that
        u ∈ ReachSet and v ∈ UnReachSet
        Edges = Edges ∪ {(u, v)}
        ReachSet = ReachSet ∪ {v}
        UnReachSet = UnReachSet - {v}
    return Edges
}
"""

CODE_FOR_PRIM_QUEUE = """PRIM(Graph) {
    Edges = ∅, UnReachSet = G.V
    set all vertices v.minEdge = ∅
    set all vertices v.key = ∞
    set an arbitrary vertex v.key = 0
    while UnReachSet ≠ ∅
        u = EXTRACT_MIN(UnReachSet)
        if u.minEdge ≠ ∅
            add u.minEdge to Edges
        for each neighbor v of u
            if v ∈ UnReachSet and
            weight(u, v) < v.key
                v.key = weight(u, v)
                v.minEdge = (u, v)
    return Edges
}
"""


CODE_FOR_KRUSKAL = """KRUSKAL_IDEA(Graph) {
    Edges = ∅
    scan all edges by nondecreasing weight
        if an edge is safe (does not form
        any cycle with the MST so far)
            add the edge to Edges
    return Edges 
}
"""

CODE_FOR_KRUSKAL_CHINESE = """KRUSKAL(Graph) {
    Edges = ∅
    按从小到大的顺序检查每条边
        如果这条边是安全的（没有和最小生成树形成任何环）
            将这条边加入 Edges
    return Edges 
}
"""


CODE_FOR_KRUSKAL_UNION_FIND = """KRUSKAL(Graph) {
    Edges = ∅
    for each vertex v ∈ G.V
        MAKE_SET(v)
    scan all edges by nondecreasing weight
    for each edge (u, v)
        if FIND_SET(u) ≠ FIND_SET(v)
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
        u = EXTRACT_MIN(UnReachSet)
        for each neighbor v of u
            RELAX(u, v, weight(u, v))
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
        u = EXTRACT_MIN(UnReachSet)
        for each neighbor v of u
            if v.key > u.key + weight(u, v)
                v.key = u.key + weight(u, v)
                v.previous = u
}
"""

CODE_FOR_DIJKASTRA_WITHOUT_RELAX_CH = """DIJKSTRA(G, s) {
    UnReachSet = G.V
    对于每一个点v设置 v.key = ∞
    对于每一个点v设置 v.previous = ∅
    对于源点s设置 s.key = 0
    while UnReachSet ≠ ∅
        v = EXTRACT_MIN(UnReachSet)
        对于从v出发的每条边(v, u)
            // 松弛边(v, u)
            if u.key > v.key + weight(u, v)
                u.key = v.key + weight(u, v)
                u.previous = v
}
"""

CODE_FOR_BELLMAN_FORD = """BELLMAN_FORD(G, s) {
    UnReachSet = G.V
    set all vertices v.key = ∞
    set all vertices v.previous = ∅
    s.key = 0
    for i = 1 to |G.V| - 1
        for each edge (u, v)
            // Relax edge (u, v)
            if v.key > u.key + weight(u, v)
                v.key = u.key + weight(u, v)
                v.previous = u
    // Check negative cycle
    for each edge (u, v)
        if v.key > u.key + weight(u, v)
            return FALSE
    return TRUE
}
"""

CODE_FOR_BELLMAN_FORD_WITH_RELAX = """BELLMAN_FORD(G, src) {
    set all vertices v.key = ∞
    set all vertices v.previous = ∅
    src.key = 0
    for i = 1 to |G.V| - 1
        for each edge (u, v)
            RELAX(u, v, weight(u, v))
    // Check for a negative cycle
    for each edge (u, v)
        if v.key > u.key + weight(u, v)
            return FALSE
    return TRUE
}
"""