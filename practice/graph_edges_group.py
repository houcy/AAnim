from manim import *
from manim_fonts import *
from style import *


class GraphEdgesGroup:
    def __init__(self, edges_array=None):
        self.mobject = VGroup()
        self.save_state = False
        if edges_array:
            for edge in edges_array:
                self.add(edge)
    
    def add(self, edge):
        self.mobject += edge.mobject["line"]

    def highlight(self, color):
        self.mobject.save_state()
        self.save_state = True
        return AnimationGroup(self.mobject.animate.set_fill(color).set_stroke(color, width=WIDTH+5), Wait(), lag_ratios=1)

    def dehighlight(self, color=GRAY):
        if self.save_state:
            self.save_state = False
            return AnimationGroup(Restore(self.mobject), Wait(), lag_ratios=1)
        else:
            return AnimationGroup(self.mobject.animate.set_fill(color).set_stroke(color, width=WIDTH), Wait(), lag_ratios=1)
