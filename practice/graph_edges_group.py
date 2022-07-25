from manim import *
from manim_fonts import *
from style import *


class GraphEdgesGroup:
    def __init__(self, edges_array=None):
        self.line_mobject = VGroup()
        self.text_mobject = VGroup()
        self.edges_array = []
        self.save_state = False
        if edges_array:
            for edge in edges_array:
                self.add(edge)
        self.mobject = VGroup()

    def get_mobject(self):
        return VGroup(self.line_mobject, self.text_mobject)

    def add(self, edge):
        self.line_mobject += edge.mobject["line"]
        self.text_mobject += edge.mobject["text"]
        self.edges_array.append(edge)

    def highlight(self, color=PINK4, width=EDGE_HIGHLIGHT_STROKE_WIDTH):
        self.line_mobject.save_state()
        self.save_state = True
        return AnimationGroup(self.line_mobject.animate.set_stroke(color=color, width=width))

    def dehighlight(self, color=GRAY):
        if self.save_state:
            self.save_state = False
            return AnimationGroup(Restore(self.line_mobject), Wait(), lag_ratio=1)
        else:
            return AnimationGroup(self.line_mobject.animate.set_stroke(color=color, width=WIDTH), Wait(), lag_ratio=1)

    def disappear(self, include_label=False):
        # self.line_mobject.save_state()
        if include_label:
            self.text_mobject.save_state()
            return AnimationGroup(AnimationGroup(FadeOut(self.line_mobject), FadeOut(self.text_mobject)), Wait(), lag_ratio=1)
        else:
            return AnimationGroup(self.line_mobject.animate.set_color(color=BACKGROUND), Wait(), lag_ratio=1)

    def appear(self, include_label=False):
        if include_label:
            return AnimationGroup(AnimationGroup(FadeIn(self.line_mobject), FadeIn(self.text_mobject)), Wait(), lag_ratio=1)
        else:
            return AnimationGroup(Restore(self.line_mobject), Wait(), lag_ratio=1)