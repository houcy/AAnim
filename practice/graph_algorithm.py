from manim import *
from style import *
from graph import Graph


MAP= {'A': ['B'],
        'B': ['D'],
        'C': ['A'],
        'D': ['C'],
        }

POSITION = {'A': (-1, 1), 'B': (1, 1), 'C': (-1, -1), 'D': (1, -1)}

class GraphAlgorithm(Scene):
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
        graph = Graph(MAP, POSITION, True)
        self.add(graph.graph_mobject)
        print(graph.value2node)
        self.dfs(graph)
    
        