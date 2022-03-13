from manim import *
from manim_fonts import *
from style import *


class GraphNodesGroup:
    def __init__(self, list_nodes=None):
        self.list_nodes = list_nodes
    
    def add(self, n):
        self.list_nodes.append(n)

    def remove(self, n):
        if n in self.list_nodes:
            self.list_nodes.remove(n)

    def key_mobject(self):
        mobject = VGroup()
        for n in self.list_nodes:
            if n.key_mobject:
                mobject += n.key_mobject
        return mobject

    def circle_mobject(self):
        mobject = VGroup()
        for n in self.list_nodes:
            if n.circle_mobject:
                mobject += n.circle_mobject
        return mobject

    def color(self, color=PINK1, width=0, scale=1):
        circle_mobject = self.circle_mobject()
        key_mobject = self.key_mobject()
        return AnimationGroup(circle_mobject.animate.set_stroke(color=color), key_mobject.animate.set_color(color=color).set_stroke(width=width))