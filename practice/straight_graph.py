from manim import *
from style import *
from graph_node import GraphNode
from graph_edge import GraphEdge

class StraightGraph:
    def __init__(self, adjacency_list, position, draw_isolated_nodes=False, is_music_note=False):
        self.graph_mobject = VGroup()
        self.value2node = {}
        self.is_directed = True
        visited_edge = set()
        self.adjacency_list = adjacency_list
        self.edges = []
        self.position = position
        self.nodes2edge = {}
        self.isolated_nodes_value2node = {}
        self.nonisolated_nodes_value2node = {}
        for start in self.adjacency_list:
            if start not in self.value2node:
                position_x, position_y = position[start]
                self._create_node(start, position_x, position_y, is_music_note=is_music_note)
            for end in self.adjacency_list[start]:
                if end not in self.value2node:
                    position_x, position_y = position[end]
                    self._create_node(end, position_x, position_y, is_music_note=is_music_note)
                if (start, end) not in visited_edge:
                    self._create_edge(start, end)
        # add isolated nodes
        for node_value in position:
            if node_value not in self.value2node:
                position_x, position_y = position[node_value]
                self._create_node(node_value, position_x, position_y, is_isolated=True, draw_isolated_nodes=draw_isolated_nodes, is_music_note=is_music_note)
        self.graph_mobject = self.graph_mobject.move_to(ORIGIN)

    def _create_node(self, value, position_x, position_y, is_isolated=False, draw_isolated_nodes=False, is_music_note=False):
        node = GraphNode(value, position_x, position_y, is_music_note=is_music_note)
        self.value2node[value] = node
        self.graph_mobject += node.mobject
        if is_isolated:
            node.is_isolated = True
            self.isolated_nodes_value2node[value] = node
            if draw_isolated_nodes:
                self.graph_mobject += node.mobject
        else:
            self.nonisolated_nodes_value2node[value] = node
            self.graph_mobject += node.mobject
        
    def _create_edge(self, start, end):
        # new
        start_node = self.value2node[start]
        end_node = self.value2node[end]
        weight = self.adjacency_list[start][end]
        edge_object = GraphEdge(start_node, end_node, weight, is_cyclic=True, is_directed=True, is_straight_graph=True)
        start_node.neighbor2edge[end_node] = edge_object
        start_node.neighbors.append(end_node)
        start_node.edges.append(edge_object)
        self.edges.append(edge_object)
        self.nodes2edge[(start_node, end_node)] = edge_object        
        self.graph_mobject += edge_object.mobject

    def highlight(self, node_name, fill_color=PINK2, stroke_color=PINK3,  stroke_width=WIDTH, text_color=BACKGROUND):
        node = self.value2node[node_name]        
        return node.color(fill_color=fill_color, stroke_color=stroke_color, stroke_width=stroke_width, text_color=text_color)

    def get_edge(self, start, end):
        return self.nodes2edge[(start, end)]
        
    def show_all_nodes(self):
        # new
        animations = [FadeIn(n.mobject) for n in list(self.value2node.values())]
        return AnimationGroup(*animations)

    def hide_isolated_nodes(self):
        # new
        animations = [FadeOut(n.mobject) for n in list(self.isolated_nodes_value2node.values())]
        return AnimationGroup(*animations)