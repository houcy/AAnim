from manim import *
from style import *
from graph_node import GraphNode

# For Testing
MAP_DIRECTED = {'A': {'B': None, 'C': None}, 'B': {'D': None, 'E': None}, 'D': {'F': None}, 'E': {'F': None}}
MAP_UNDIRECTED = {'A': {'B': None, 'C': None}, 'B': {'A': None, 'D': None, 'E': None}, 'C': {'A': None}, 'D': {'B': None, 'F': None}, 'E': {'B': None}, 'F': {'D': None}}
MAP_DIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'D': 7, 'E': 7}, 'D': {'F': 7}, 'E': {'F': 7}}
MAP_UNDIRECTED_WEIGHT = {'A': {'B': 7, 'C': 7}, 'B': {'A': 7, 'D': 7, 'E': 7}, 'C': {'A': 7}, 'D': {'B': 7, 'F': 7}, 'E': {'B': 7}, 'F': {'D': 7}}
POSITION1 = {'A': (1.2692307692307692, 3.0), 'B': (0.8076923076923077, 2.076923076923077), 'C': (1.7307692307692308, 2.076923076923077), 'D': (0.34615384615384615, 1.1538461538461537), 'E': (1.2692307692307692, 1.1538461538461537), 'F': (0.34615384615384615, 0.23076923076923078)}

class Graph:
    def __init__(self, adjacency_list, position, is_directed=False, is_topological_graph=False):
        self.graph_mobject = VGroup()
        self.value2node = {}
        self.is_directed = is_directed
        visited_edge = set()
        self.adjacency_list = adjacency_list
        self.position = position
        for start in adjacency_list:
            if start not in self.value2node:
                position_x, position_y = position[start]
                self._create_node(start, position_x, position_y)
                
            for end in adjacency_list[start]:
                if end not in self.value2node:
                    position_x, position_y = position[end]
                    self._create_node(end, position_x, position_y)
                if (start, end) not in visited_edge:
                    visited_edge.add((end, start))
                    self._create_edge(start, end, is_directed, is_topological_graph)
                    
        self.graph_mobject = self.graph_mobject.move_to(ORIGIN)
                
    def _create_node(self, value, position_x, position_y):
        node = GraphNode(value, position_x, position_y)
        self.value2node[value] = node
        self.graph_mobject += node.mobject

    def _create_edge(self, start, end, is_directed, is_topological_graph):
        start_node = self.value2node[start]
        end_node = self.value2node[end]
        line = None
        edge_value = None
        if not is_directed:
            line = Line(start_node.mobject.get_center(), end_node.mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        elif is_topological_graph:
            line = CurvedArrow(start_node.mobject.get_bottom(), end_node.mobject.get_bottom(), color=LINE_COLOR, stroke_width=WIDTH).set_z_index(0)
        else:
            line = Line(start_node.mobject.get_center(), end_node.mobject.get_center(), buff=0.4, stroke_width=WIDTH).add_tip(tip_length=0.05).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        # If there's a weight
        if self.adjacency_list[start][end]:
            edge_value = self.adjacency_list[start][end]
            text = Text(str(edge_value), color=PINK1, font=FONT, weight="HEAVY", font_size=EDGE_WEIGHT_SIZE).move_to(line.get_center()).set_z_index(1).set_stroke(color=BACKGROUND, width=2)
            self.graph_mobject += text

        start_node.neighbor2line[end_node] = line
        if not is_directed:
            end_node.neighbor2line[start_node] = line
        self.graph_mobject += line
        

class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        graph = Graph(MAP_UNDIRECTED, POSITION1, is_directed=False)
        self.add(graph.graph_mobject)
        self.play(FadeOut(graph.graph_mobject))
        graph = Graph(MAP_DIRECTED, POSITION1, is_directed=True)
        self.add(graph.graph_mobject)
        self.play(FadeOut(graph.graph_mobject))
        graph = Graph(MAP_UNDIRECTED_WEIGHT, POSITION1, is_directed=False)
        self.add(graph.graph_mobject)
        self.play(FadeOut(graph.graph_mobject))
        graph = Graph(MAP_DIRECTED_WEIGHT, POSITION1, is_directed=True)
        self.add(graph.graph_mobject)
        self.play(FadeOut(graph.graph_mobject))
    