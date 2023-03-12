from manim import *
from manim_fonts import *
from style import *
from util import *
from graph_node import GraphNode

# z_index: edge: 0, circle: 1, text: 3, key: 5
class TreeNode(GraphNode):
    def __init__(self, value, position_x, position_y):
        GraphNode.__init__(self, value, position_x, position_y)
        self.left = None
        self.right = None