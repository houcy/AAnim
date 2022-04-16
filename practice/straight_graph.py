from manim import *
from style import *
from music import *
import math
from graph_node import GraphNode
from graph_edge import GraphEdge

class StraightGraph:
    def __init__(self, adjacency_list, values, is_music_note=False):
        self.node_mobject = VGroup()
        self.edge_mobject = VGroup()
        self.value2node = {}
        self.is_directed = True
        visited_edge = set()
        self.adjacency_list = adjacency_list
        self.edges = []
        self.values = values
        self.value2index = {}
        self.curr_center_index = None
        for i, value in enumerate(values):
            self.value2index[value] = i
        self.nodes2edge = {}
        positions = generate_positions(values)
        for node_value in values:
            position_x, position_y = positions[node_value]
            self._create_node(node_value, position_x, position_y, is_music_note=is_music_note)
        self.curr_center_index = (self.n_nodes() - 1) // 2
        # for n in self.nodes2edge:
        #     print(n.get_center())
        for start in self.adjacency_list:
            for end in self.adjacency_list[start]:
                if (start, end) not in visited_edge:
                    self._create_edge(start, end)
                    visited_edge.add((start, end))
                    start_node = self.value2node[start]
                    end_node = self.value2node[end]
                    start_node.is_isolated = False
                    end_node.is_isolated = False

    def _create_node(self, value, position_x, position_y, is_music_note=False):
        node = GraphNode(value, position_x, position_y, is_music_note=is_music_note)
        self.value2node[value] = node
        self.node_mobject += node.mobject
        
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
        self.edge_mobject += edge_object.mobject

    def mobject(self):
        return VGroup(self.node_mobject, self.edge_mobject)

    def highlight(self, node_name, fill_color=PINK2, stroke_color=PINK3,  stroke_width=WIDTH, text_color=BACKGROUND):
        node = self.value2node[node_name]        
        return node.color(fill_color=fill_color, stroke_color=stroke_color, stroke_width=stroke_width, text_color=text_color)

    def get_edge(self, start, end):
        return self.nodes2edge[(start, end)]

    def get_nodes(self):
        return list(self.value2node.values())
        
    def n_nodes(self):
        return len(self.value2node)

    def show_all_nodes(self):
        # new
        node_animations = []
        for n in list(self.value2node.values()):
            if n.is_showing == False:
                node_animations.append(FadeIn(n.mobject))
                n.is_showing = True
        return AnimationGroup(*node_animations)

    def show_all_edges(self):
        # new
        edge_animations = []
        for e in self.edges:
            if e.is_showing == False:
                edge_animations.append(FadeIn(e.mobject))
                e.is_showing = True
        return AnimationGroup(*edge_animations)

    def hide_all_nodes(self):
        # new
        node_animations = []
        for n in list(self.value2node.values()):
            if n.is_showing == True:
                node_animations.append(FadeOut(n.mobject))
                n.is_showing = False
        return AnimationGroup(*node_animations)

    def hide_all_edges(self):
        # new
        edge_animations = []
        for e in self.edges:
            if e.is_showing == True:
                edge_animations.append(FadeOut(e.mobject))
                e.is_showing = False
        return AnimationGroup(*edge_animations)

    def show_all_nodes_and_edges(self):
        # new
        node_animations = [FadeIn(n.mobject) for n in list(self.value2node.values())]
        edge_animations = [FadeIn(e.mobject) for e in self.edges]
        return AnimationGroup(*node_animations, *edge_animations)

    def show_all_hidden_nodes(self):
        node_animations = []
        for n in list(self.value2node.values()):
            if n.is_showing == False:
                node_animations.append(FadeIn(n.mobject))
                n.is_showing = True
        return AnimationGroup(*node_animations)
        
    def hide_nodes_not_in(self, start_value, end_value):
        # hide all nodes before start or after end (start and end are not included)
        start_index = self.value2index[start_value]
        end_index = self.value2index[end_value]
        animations = []
        for i in range(0, start_index):
            node = self.value2node[self.values[i]]
            animations.append(FadeOut(node.mobject))
            node.is_showing = False
        for i in range(end_index+1, self.n_nodes()-1):
            node = self.value2node[self.values[i]]
            animations.append(FadeOut(node.mobject))
            node.is_showing = False
        return AnimationGroup(*animations)

    def show(self, start_value, end_value):
        start_index = self.value2index[start_value]
        end_index = self.value2index[end_value]
        mid_index = (start_index + end_index) / 2
        step_length = NODE_BUFF
        offset = (self.curr_center_index - mid_index) * step_length
        self.mobject().shift(offset*RIGHT)
        self.curr_center_index = mid_index
        animations = []
        for i in range(start_index, end_index+1):
            node = self.value2node[self.values[i]]
            animations.append(FadeIn(node.mobject))
            node.is_showing = True
        return AnimationGroup(*animations)
    
    def shift(self, start_value, end_value):
        # fadein_animation = self.show_all_hidden_nodes()
        start_index = self.value2index[start_value]
        end_index = self.value2index[end_value]
        mid_index = (start_index + end_index) / 2
        step_length = NODE_BUFF
        offset = (self.curr_center_index - mid_index) * step_length
        shift_animations = [n.mobject.animate.shift(offset*RIGHT) for n in self.get_nodes()]
        shift_animation = AnimationGroup(*shift_animations)
        for e in self.edges:
            e.mobject.shift(offset*RIGHT)
        # shift_animation = self.mobject().animate.shift(offset*RIGHT)

        self.curr_center_index = mid_index
        return shift_animation

    # def hide_isolated_nodes(self):
    #     # new
    #     animations = [FadeOut(n.mobject) for n in list(self.isolated_nodes_value2node.values())]
    #     return AnimationGroup(*animations)