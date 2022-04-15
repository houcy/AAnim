from manim import *
from manim_fonts import *
from style import *
from curved_arrow import Curved_Arrow


class GraphEdge:
    def __init__(self, start_node, end_node, weight=None, is_cyclic=False, is_directed=False, is_topological_graph=False, is_straight_graph=False, edge_radius=EDGE_RADIUS):
        line = None
        self.weight = weight
        self.start_node = start_node
        self.end_node = end_node
        self.is_directed = is_directed
        self.save_state = False
        self.visit_count = 0
        if not is_directed:
            line = Line(start_node.mobject.get_center(), end_node.mobject.get_center()).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        else:
            if is_straight_graph:
                start_position = start_node.position_x
                end_position = end_node.position_x
                if start_position < end_position:
                    line = Curved_Arrow(start_node.mobject.get_bottom(), end_node.mobject.get_bottom(), color=LINE_COLOR, stroke_width=WIDTH, edge_radius=edge_radius).mobject.set_z_index(0)
                else:
                    line = Curved_Arrow(start_node.mobject.get_top(), end_node.mobject.get_top(), color=LINE_COLOR, stroke_width=WIDTH, edge_radius=edge_radius).mobject.set_z_index(0)
            elif is_topological_graph:
                line = Curved_Arrow(start_node.mobject.get_bottom(), end_node.mobject.get_bottom(), color=LINE_COLOR, stroke_width=WIDTH, edge_radius=edge_radius).mobject.set_z_index(0)
            else:
                if is_cyclic:
                    line = Curved_Arrow(start_node.mobject.get_center(), end_node.mobject.get_center(), color=LINE_COLOR, stroke_width=WIDTH, edge_radius=edge_radius).mobject.scale(0.78).set_z_index(0)
                else:
                    # normal
                    line = Line(start_node.mobject.get_center(), end_node.mobject.get_center(), buff=0.4, stroke_width=WIDTH).add_tip(tip_length=TIP_LENGTH_FOR_STRAIGHT_LINE).set_stroke(color=LINE_COLOR, width=WIDTH).set_z_index(0)
        self.mobject = VDict([("line", line)])

        # for weighted edge
        if self.weight:
            text = Text(str(weight), color=EDGE_COLOR, font=FONT, weight=WEIGHT_WEIGHT, font_size=WEIGHT_SIZE).move_to(line.get_center()).set_z_index(10).set_stroke(color=EDGE_STROKE_COLOR, width=EDGE_STROKE_WIDTH)
            text_background = Circle(radius=WEIGHT_CIRCLE_RADIUS).set_stroke(color=BACKGROUND, width=WIDTH).set_fill(BACKGROUND, opacity=1.0).set_z_index(9).move_to(text.get_center())
            self.mobject["text"] = VDict([("text", text), ("text_background", text_background)])

    def get_the_other_end(self, node):
        if node == self.start_node:
            return self.end_node
        elif node == self.end_node:
            return self.start_node
        else:
            print("Failed to output the other end of the edge, the input node is incorrect")
            return None

    def highlight(self, color=PINK4, width=EDGE_HIGHLIGHT_STROKE_WIDTH, change_tip_width=True):
        self.mobject["line"].save_state()
        self.save_state = True
        if change_tip_width:
            return AnimationGroup(self.mobject["line"].animate.set_stroke(width=width).set_color(color=color))
        else:
            return AnimationGroup(self.mobject["line"].animate.set_color(color=color))


    def dehighlight(self, color=GRAY, force_color=False):
        if self.save_state and not force_color:
            self.save_state = False
            return AnimationGroup(Restore(self.mobject["line"]))
        else:
            return AnimationGroup(self.mobject["line"].animate.set_stroke(color=color, width=WIDTH))

    def fade_out(self):
        return FadeOut(self.mobject)

    def fade_in(self):
        return FadeIn(self.mobject)
