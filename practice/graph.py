from manim import *
from style import *
from graph_node import GraphNode


class Graph:
    def __init__(self, adjacency_list, position, is_directed=False):
        self.graph_mobject = VGroup()
        self.value2node = {}
        for start in adjacency_list:
            if start not in self.value2node:
                position_x, position_y = position[start]
                self._create_node(start, position_x, position_y)
                
            for end in adjacency_list[start]:
                if end not in self.value2node:
                    position_x, position_y = position[end]
                    self._create_node(end, position_x, position_y)
                self._create_edge(start, end, is_directed)
        self.graph_mobject = self.graph_mobject.move_to(ORIGIN)
                
    def _create_node(self, value, position_x, position_y):
        node = GraphNode(value, position_x, position_y)
        self.value2node[value] = node
        self.graph_mobject += node.mobject

    def _create_edge(self, start, end, is_directed):
        start_node = self.value2node[start]
        end_node = self.value2node[end]
        line = None
        if not is_directed:
            line = Line(start_node.mobject.get_center(), end_node.mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        else:
            line = Arrow(start_node.mobject.get_center(), end_node.mobject.get_center(), buff=0.4, max_tip_length_to_length_ratio=0.1).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        start_node.neighbor2line[end_node] = line
        self.graph_mobject += line



