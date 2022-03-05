from turtle import width
from manim import *
from manim_fonts import *
from style import *


class GraphEdgesGroup:
    def __init__(self):
        self.mobject = VGroup()
    
    def add(self, mobject):
        self.mobject += mobject["line"]

    def highlight(self, color):
        return AnimationGroup(self.mobject.animate.set_fill(color).set_stroke(color, width=WIDTH+5), Wait())

    def dehighlight(self, color=GRAY):
        return AnimationGroup(self.mobject.animate.set_fill(color).set_stroke(color, width=WIDTH), Wait())