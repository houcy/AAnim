from manim import *
from style import *
from graph import Graph
from code_block import CodeBlock


MAP= {'A': ['B'], 'B': ['D'], 'D': ['C'], 'C': ['A']}

POSITION = {'A': (-1, 1), 'B': (1, 1), 'C': (-1, -1), 'D': (1, -1)}

POSITION2 = {'A': (0.675, 2.1569), 'B': (2.4143499999999998, 0.45), 'D': (4.135, 2.181125), 'C': (2.38995, 3.8865000000000003)}

CODE_FOR_DFS = """DFS(G) {
    for each vertex u
        if u.color = BLACK
            DFS-VISIT(G, u)
}

DFS-VISIT(G, u) {
    u.color = PINK
    for each v in G.Adj[u]
        if v.color = BLACK
            DFS-VISIT(G, v)
    u.color = BLUE
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
        self.play(node.mark_discovered())
        self.play(code_block.highlight(9))
        for neighbor in node.neighbor2line:
            self.play(code_block.highlight(10))
            if neighbor not in discovered:
                self.play(code_block.highlight(11))
                self.play(node.mark_line_discovered(neighbor))
                self._dfs_helper(neighbor, discovered, code_block)
                self.play(node.mark_line_finished(neighbor))
        self.play(code_block.highlight(12))
        self.play(node.mark_finished())

    def dfs(self, graph, code_block, source=None, dest=None):
        discovered = set()
        self.play(code_block.highlight(1))
        if not source:    # Traverse all
            self.play(code_block.highlight(2))
            for vertex in graph.value2node:
                node = graph.value2node[vertex]
                self.play(code_block.highlight(3))
                if node not in discovered:
                    self.play(code_block.highlight(4))
                    self._dfs_helper(node, discovered, code_block)
        else:   # Stop when finding out dest
            pass

        self.play(code_block.highlight(5))
        self.play(FadeOut(code_block.code))
            
    def construct(self):
        self.camera.background_color = BACKGROUND
        graph = Graph(MAP, POSITION2, True)
        # graph = Graph(self.adjacency_list, self.position, self.is_directed)
        code_block = CodeBlock(CODE_FOR_DFS)
        self.add(graph.graph_mobject.shift(2 * RIGHT))
        self.add(code_block.code)
        self.dfs(graph, code_block)
    
        