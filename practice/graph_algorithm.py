from manim import *
from style import *
from graph import Graph
from code_block import CodeBlock
from legend import Legend


MAP= {'A': ['B'], 'B': ['D'], 'D': ['C'], 'C': ['A']}

POSITION1 = {'A': (0.675, 2.1569), 'B': (2.4143499999999998, 0.45), 'D': (4.135, 2.181125), 'C': (2.38995, 3.8865000000000003)}

MAP2 = {'A': ['B', 'C'], 'B': ['A', 'D', 'E'], 'C': ['A'], 'D': ['B', 'F'], 'E': ['B'], 'F': ['D']}

POSITION2 = {'A': (1.2692307692307692, 3.0), 'B': (0.8076923076923077, 2.076923076923077), 'C': (1.7307692307692308, 2.076923076923077), 'D': (0.34615384615384615, 1.1538461538461537), 'E': (1.2692307692307692, 1.1538461538461537), 'F': (0.34615384615384615, 0.23076923076923078)}

CODE_FOR_DFS = """DFS(G) {
    for each vertex u
        if u.color = BLACK
            DFS-VISIT(G, u)
}

DFS-VISIT(G, u) {
    u.color = BLUE
    for each v in G.Adj[u]
        if v.color = BLACK
            DFS-VISIT(G, v)
    u.color = PINK
}
"""

CODE_FOR_BFS = """BFS(G, s) {
    s.color = BLUE
    Q = Φ
    ENQUEUE(Q, s)
    while Q != Φ
        u = DEQUEUE(Q)
        for each v in G.adj[u]
            if v.color = BLACK
                v.color = BLUE
                ENQUEUE(Q, v)
        u.color = PINK
}
"""

class GraphAlgorithm(Scene):
    # def __init__(self, adjacency_list, position, is_directed):
    #     self.adjacency_list = adjacency_list
    #     self.position = position
    #     self.is_directed = is_directed
    #     super().__init__()

    def _dfs_helper(self, node, discovered, code_block):
        self.play(code_block.highlight(7))
        discovered.add(node)
        self.play(code_block.highlight(8))
        self.play(node.mark_pink1())
        self.play(code_block.highlight(9))
        for neighbor in node.neighbor2line:
            self.play(code_block.highlight(10))
            if neighbor not in discovered:
                self.play(code_block.highlight(11))
                self.play(node.mark_line_pink1(neighbor))
                self._dfs_helper(neighbor, discovered, code_block)
                self.play(node.mark_line_finished(neighbor))
        self.play(code_block.highlight(12))
        self.play(node.mark_finished())

    def dfs(self, graph, code_block):
        """
        DFS on the graph to traver every node
        """
        discovered = set()
        self.play(code_block.highlight(1))
        self.play(code_block.highlight(2))
        for vertex in graph.value2node:
            node = graph.value2node[vertex]
            self.play(code_block.highlight(3))
            if node not in discovered:
                self.play(code_block.highlight(4))
                self._dfs_helper(node, discovered, code_block)
        self.play(code_block.highlight(5))
        self.play(FadeOut(code_block.code))

    def bfs(self, graph, s, code_block):
        """
        BFS on the graph to find every vertex that is reacheable from s
        ?Why?
        """
        discovered = set()
        queue = []
        s_node = graph.value2node[s]
        queue.append(s_node)
        discovered.add(s_node)
        self.play(s_node.mark_pink1())
        while queue:
            curr = queue.pop(0)
            for neighbor in curr.neighbor2line:
                if neighbor not in discovered:
                    queue.append(neighbor)
                    discovered.add(curr)
                    self.play(neighbor.mark_pink1())
            self.wait(1)
            self.play(curr.mark_finished())

    def mark_levels(self, level, color):
        animation = []
        for node in level:
            animation.append(node.mobject["c"].animate.set_fill(color).set_stroke(color))
            animation.append(node.mobject["t"].animate.set_color(BACKGROUND))
        return AnimationGroup(*animation)
    

    def bfs2(self, graph, s, code_block):
        """
        BFS on the graph to find every vertex that is reacheable from s
        ?Why?
        """
        l = Legend({PINK1: "curr level", PINK3: "next level", BLUE1: "finished"})
        l.mobjects.next_to(graph.graph_mobject, RIGHT, buff=0.5)
        self.play(l.animation)
        discovered = set()
        curr_level = []
        next_level = []
        s_node = graph.value2node[s]
        curr_level.append(s_node)
        discovered.add(s_node)
        self.play(s_node.mark_pink1())
        while curr_level:
            for curr in curr_level:
                for neighbor in curr.neighbor2line:
                    if neighbor not in discovered:
                        next_level.append(neighbor)
                        discovered.add(curr)
                        self.play(neighbor.mark_pink3())
                self.wait(1)
            self.play(self.mark_levels(curr_level, BLUE1))
            curr_level = next_level
            next_level = []
            self.play(self.mark_levels(curr_level, PINK1))
            

    def construct(self):
        self.camera.background_color = BACKGROUND
        graph = Graph(MAP2, POSITION2, False)
        # graph = Graph(self.adjacency_list, self.position, self.is_directed)
        self.add(graph.graph_mobject.shift(1.8 * RIGHT))
    # Comment out DFS code
        # code_block = CodeBlock(CODE_FOR_DFS)
        # self.add(code_block.code)
        # self.dfs(graph, code_block)
        
        code_block_bfs = CodeBlock(CODE_FOR_BFS)
        self.add(code_block_bfs.code)
        self.bfs2(graph, 'A', code_block_bfs)
    
        