from manim import *
from style import *
from graph_node import GraphNode


class Graph:
    def __init__(self, adjacency_list, position, edge_value=None, is_directed=False, is_topological_graph=False):
        self.graph_mobject = VGroup()
        self.value2node = {}
        self.is_directed = is_directed
        visited_edge = set()
        self.adjacency_list = None
        if edge_value:
            self.adjacency_list = edge_value
        else:
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
                    self._create_edge(start, end, is_directed, edge_value, is_topological_graph)

                    
        self.graph_mobject = self.graph_mobject.move_to(ORIGIN)
                
    def _create_node(self, value, position_x, position_y):
        node = GraphNode(value, position_x, position_y)
        self.value2node[value] = node
        self.graph_mobject += node.mobject

    def _create_edge(self, start, end, is_directed, edge_value, is_topological_graph):
        start_node = self.value2node[start]
        end_node = self.value2node[end]
        line = None
        if not is_directed:
            line = Line(start_node.mobject.get_center(), end_node.mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        elif is_topological_graph:
            line = CurvedArrow(start_node.mobject.get_bottom(), end_node.mobject.get_bottom(), color=LINE_COLOR, stroke_width=WIDTH).set_z_index(0)
        else:
            line = Line(start_node.mobject.get_center(), end_node.mobject.get_center(), buff=0.4, stroke_width=WIDTH).add_tip(tip_length=0.05).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        if edge_value:
            value = 0
            if start in edge_value and end in edge_value[start]:
                value = edge_value[start][end]
            elif end in edge_value and start in edge_value[end]:
                value = edge_value[end][start]
            else:
                print("Failed to get value from edge_value")
                return
            text = Text(str(value), color=PINK1, font=FONT, weight="HEAVY", font_size=EDGE_WEIGHT_SIZE).move_to(line.get_center()).set_z_index(1).set_stroke(color=BACKGROUND, width=2)
            self.graph_mobject += text

        start_node.neighbor2line[end_node] = line
        end_node.neighbor2line[start_node] = line
        self.graph_mobject += line



