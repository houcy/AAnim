from manim import *
from manim_fonts import *
from style import *
from curved_arrow import Curved_Arrow
from util import *


class GeneralEdge:
    def __init__(self, start, end, weight='', font_weight=HEAVY, buff=0, width=WIDTH, font_size=WEIGHT_SIZE, line_mobject=None, is_cyclic=False, is_directed=False, edge_radius=EDGE_RADIUS, color=GRAY, zoom_in_power=1):
        self.weight = weight
        self.start_mobject = start.mobject
        self.end_mobject = end.mobject
        self.is_directed = is_directed
        self.is_curvy = False
        self.save_state = False
        self.visit_count = 0
        self.is_showing = False
        self.name = start.name + end.name
        if not line_mobject:
            if not is_directed:
                line_mobject = Line(self.start_mobject.get_center(), self.end_mobject.get_center(), buff=buff).set_stroke(color=color, width=width).set_z_index(0)
            else:
                if is_cyclic:
                    line_mobject = Curved_Arrow(self.start_mobject.get_center(), self.end_mobject.get_center(), color=color, stroke_width=width, edge_radius=edge_radius).mobject.scale(0.78).set_z_index(0)
                    self.is_curvy = True
                else:
                    # normal
                    line_mobject = Line(self.start_mobject.get_center(), self.end_mobject.get_center(), buff=0.4, stroke_width=width).add_tip(tip_length=TIP_LENGTH_FOR_STRAIGHT_LINE, tip_width=TIP_LENGTH_FOR_STRAIGHT_LINE).set_stroke(color=color, width=WIDTH).set_z_index(0)
        self.mobject = VDict([("line", line_mobject)])

        # for weighted edge
        if self.weight:
            text = get_text(weight, color=GRAY, weight=font_weight, font_size=font_size/zoom_in_power).move_to(line_mobject.get_center()).set_z_index(10).set_stroke(color=EDGE_STROKE_COLOR, width=EDGE_STROKE_WIDTH/zoom_in_power)
            text_background = SurroundingRectangle(text, corner_radius=0.2, buff=0.05).set_fill(BACKGROUND, opacity=1.0).set_stroke(color=BACKGROUND).set_z_index(9)
            self.mobject["text"] = VDict([("text", text), ("text_background", text_background)])

    def highlight(self, color=PINK4, width=EDGE_HIGHLIGHT_STROKE_WIDTH, change_tip_width=True):
        # if self.is_directed:
        #     if self.is_curvy:
        #         width = EDGE_HIGHLIGHT_STROKE_WIDTH_FOR_DIGRAPH_CURVY
        #     else:
        #         width = EDGE_HIGHLIGHT_STROKE_WIDTH_FOR_DIGRAPH
        self.mobject["line"].save_state()
        self.save_state = True
        if self.is_directed and change_tip_width:
            print(0)
            return AnimationGroup(self.mobject["line"].animate.set_stroke(width=width).set_color(color=color))
        else:
            # if self.weight:
            #     return AnimationGroup(self.mobject["line"].animate.set_color(color=color).set_stroke(width=width), self.mobject["text"]["text"].animate.set_color(color=color))
            # else:
            return AnimationGroup(self.mobject["line"].animate.set_color(color=color).set_stroke(width=width))


    def dehighlight(self, color=GRAY, force_color=False):
        if self.save_state and not force_color:
            self.save_state = False
            return AnimationGroup(Restore(self.mobject["line"]))
        else:
            return AnimationGroup(self.mobject["line"].animate.set_stroke(color=color, width=WIDTH))

    def fade_out(self):
        self.is_showing = False
        return FadeOut(self.mobject)

    def fade_in(self):
        self.is_showing = True
        return FadeIn(self.mobject)

    def fade_in_sequence(self):
        self.is_showing = True
        return Succession(FadeIn(self.mobject['line']), FadeIn(self.mobject['text']))