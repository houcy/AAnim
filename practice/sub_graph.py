from manim import *
from style import *
from graph_node import GraphNode
from graph_edge import GraphEdge
from graph_edges_group import GraphEdgesGroup
from graph_nodes_group import GraphNodesGroup
from util import *


class SubGraph:
    def __init__(self, edges_list, node_list):
        self.nodes_group = GraphNodesGroup(node_list)
        self.edges_group = GraphEdgesGroup(edges_list)
        self.nodes = node_list
        self.edges = edges_list

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def highlight(self, node_text_color=BACKGROUND, node_fill_color=PINK4, node_stroke_color=PINK5, edge_color=GRAY, edge_width=EDGE_HIGHLIGHT_STROKE_WIDTH, together=True, lag_ratio=0.1):
        if together:
            return AnimationGroup(
                self.nodes_group.highlight(text_color=node_text_color, fill_color=node_fill_color, stroke_color=node_stroke_color),
                self.edges_group.highlight(color=edge_color, width=edge_width)
            )
        else:
            animations = []
            for node in self.get_nodes():
                animations.append(node.color(stroke_color=node_stroke_color, fill_color=node_fill_color))
            for edge in self.get_edges():
                animations.append(edge.highlight(color=edge_color, width=edge_width))
            return Succession(*animations, lag_ratio=lag_ratio)

    def dehighlight(self, together=True):
        if together:
            return AnimationGroup(
                self.nodes_group.dehighlight(text_color=node_text_color, fill_color=node_fill_color, stroke_color=node_stroke_color),
                self.edges_group.highlight(color=edge_color, width=edge_width)
            )
