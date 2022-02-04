from manim import *
from style import *
from graph import Graph


MAP= {'A': ['B', 'C'], 'B': ['A', 'D'], 'D': ['B', 'C'], 'C': ['A', 'D']}

POSITION = {'A': (-1, 1), 'B': (1, 1), 'C': (-1, -1), 'D': (1, -1)}

POSITION2 = {'A': (0.675, 2.1569), 'B': (2.4143499999999998, 0.45), 'D': (4.135, 2.181125), 'C': (2.38995, 3.8865000000000003)}

class GraphAlgorithm(Scene):
    def __init__(self, adjacency_list, position):
        self.adjacency_list = adjacency_list
        self.position = position
        super().__init__()

    def _dfs_helper(self, node, discovered):
        discovered.add(node)
        self.play(node.mark_discovered())
        for neighbor in node.neighbor2line:
            if neighbor not in discovered:
                self._dfs_helper(neighbor, discovered)
        self.play(node.mark_finished())

    def dfs(self, graph, source=None, dest=None):
        discovered = set()
        if not source:    # Traverse all
            for vertex in graph.value2node:
                node = graph.value2node[vertex]
                if node not in discovered:
                    self._dfs_helper(node, discovered)
 
        else:   # Stop when visiting dest
            pass
            
    def construct(self):
        self.camera.background_color = BACKGROUND
        # graph = Graph(MAP, POSITION2, True)
        graph = Graph(self.adjacency_list, self.position, True)
        self.add(graph.graph_mobject)
        self.dfs(graph)
    
        