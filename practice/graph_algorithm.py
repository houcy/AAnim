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
    s.color = PINK
    Q = Φ
    ENQUEUE(Q, s)
    while Q != Φ
        u = DEQUEUE(Q)
        u.color = PINK
        for each v in G.adj[u]
            if v.color = BLACK
                v.color = WHITE
                ENQUEUE(Q, v)
        u.color = BLUE
}
"""

CODE2_FOR_BFS = """BFS(G, s) {
curr_level = Φ
next_level = Φ
ENQUEUE(curr_level, s)
s.color = PINK
while curr_level != Φ
    for each u in curr_level:
        for each v in G.adj[u]
            if v.color = BLACK
                ENQUEUE(next_level, v)
                v.color = WHITE
    u.color = BLUE
    curr_level = next_level
    mark PINK for all v in curr_level
    next_level = Φ
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
                self.play(node.mark_line_blue1(neighbor))
        self.play(code_block.highlight(12))
        self.play(node.mark_blue1())

    def dfs(self, graph, show_topological_sort=False):
        """
        DFS on the graph to traver every node
        """
        code_block = CodeBlock(CODE_FOR_DFS)
        self.add(code_block.code)
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

    # Mirror DFS on coloring (same with CLRS) doesn't look very clear so comment out
    # def bfs(self, graph, s):
    #     """
    #     BFS: mark 2 colors for discovered, and finished
    #     """
        # code_block = CodeBlock(CODE_FOR_BFS)
        # self.add(code_block)
    #     discovered = set()
    #     queue = []
    #     s_node = graph.value2node[s]
    #     queue.append(s_node)
    #     discovered.add(s_node)
    #     self.play(s_node.mark_pink1())
    #     while queue:
    #         curr = queue.pop(0)
    #         for neighbor in curr.neighbor2line:
    #             if neighbor not in discovered:
    #                 queue.append(neighbor)
    #                 discovered.add(curr)
    #                 self.play(neighbor.mark_pink1())
    #         self.wait(1)
    #         self.play(curr.mark_pink1())

    def mark_levels(self, level, color):
        animation = []
        for node in level:
            animation.append(node.mobject["c"].animate.set_fill(color).set_stroke(color))
            animation.append(node.mobject["t"].animate.set_color(BACKGROUND))
        return AnimationGroup(*animation)
    

    def bfs2(self, graph, s):
        """
        BFS: traverse the tree starting from source s. 
        Mark 3 colors for curr level, next level, and finished
        """
        code_block = CodeBlock(CODE2_FOR_BFS)
        self.add(code_block.code)
        self.play(code_block.highlight(1))
        l = Legend({PINK1: "curr level", PINK3: "next level", BLUE1: "finished"})
        l.mobjects.next_to(graph.graph_mobject, RIGHT, buff=0.5)
        self.play(l.animation)
        discovered = set()
        s_node = graph.value2node[s]
        curr_level = []
        self.play(code_block.highlight(2))
        next_level = []
        self.play(code_block.highlight(3))
        curr_level.append(s_node)
        self.play(code_block.highlight(4))
        discovered.add(s_node)
        self.play(code_block.highlight(5))
        self.play(s_node.mark_pink1())
        while curr_level:
            self.play(code_block.highlight(6))
            for curr in curr_level:
                self.play(code_block.highlight(7))
                self.play(curr.mobject.animate.set_stroke(color=GREEN))
                for neighbor in curr.neighbor2line:
                    self.play(code_block.highlight(8))
                    if neighbor not in discovered:
                        self.play(code_block.highlight(9))
                        next_level.append(neighbor)
                        self.play(code_block.highlight(10))
                        discovered.add(curr)
                        self.play(code_block.highlight(11))
                        self.play(neighbor.mark_pink3())
                self.play(curr.mobject.animate.set_stroke(color=PINK1))
                self.wait(1)
                self.play(code_block.highlight(12))
                self.play(curr.mark_blue1())
            self.play(code_block.highlight(13))
            # self.play(self.mark_levels(curr_level, BLUE1))
            curr_level = next_level
            self.play(code_block.highlight(14))
            self.play(self.mark_levels(curr_level, PINK1))
            next_level = []
            self.play(code_block.highlight(15))
        self.play(code_block.highlight(16))
            

    def construct(self):
        self.camera.background_color = BACKGROUND
        graph = Graph(MAP2, POSITION2, False)
        # graph = Graph(self.adjacency_list, self.position, self.is_directed)
        self.add(graph.graph_mobject.shift(1.8 * RIGHT))
    # Comment out DFS code
        self.dfs(graph)

    # # Comment out BFS code  
    #     self.bfs2(graph, 'A')
    
        