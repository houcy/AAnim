from turtle import width
from manim import *
from manim_fonts import *
from style import *


class GraphEdge:
    def __init__(self, start_node, end_node, weight=None, is_cyclic=False, is_directed=False, is_topological_graph=False):
        line = None
        self.weight = weight
        self.start_node = start_node
        self.end_node = end_node
        self.is_directed = is_directed
        if not is_directed:
            line = Line(start_node.mobject.get_center(), end_node.mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        else:
            if is_topological_graph:
                line = CurvedArrow(start_node.mobject.get_bottom(), end_node.mobject.get_bottom(), color=LINE_COLOR, stroke_width=WIDTH).set_z_index(0)
            else:
                if is_cyclic:
                    line = CurvedArrow(start_node.mobject.get_center(), end_node.mobject.get_center(), color=LINE_COLOR, stroke_width=WIDTH).scale(0.8).set_z_index(0)
                else:
                    line = Line(start_node.mobject.get_center(), end_node.mobject.get_center(), buff=0.4, stroke_width=WIDTH).add_tip(tip_length=0.05).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        self.mobject = VDict([("line", line)])

        # If it's a weighted edge
        if self.weight:
            text = Text(str(weight), color=PINK1, font=FONT, weight="HEAVY", font_size=EDGE_WEIGHT_SIZE).move_to(line.get_center()).set_z_index(1).set_stroke(color=BACKGROUND, width=2)
            self.mobject["text"] = text

    def get_the_other_end(self, node):
        if node == self.start_node:
            return self.end_node
        elif node == self.end_node:
            return self.start_node
        else:
            print("Failed to output the other end of the edge, the input node is incorrect")
            return None

    def mark_color(self, color):
        return AnimationGroup(self.mobject["line"].animate.set_fill(color).set_stroke(color, width=WIDTH+5), Wait())