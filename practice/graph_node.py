from manim import *
from manim_fonts import *
from style import *


class GraphNode:
    def __init__(self, value, position_x, position_y):
        self.value = value
        self.neighbor2edge = {}
        self.edges = []
        self.position_x = position_x
        self.position_y = position_y
        self.mobject = None
        self.text_mobject = self._create_text_mobject(value)
        self._create_mobject()
    
    def _create_mobject(self):
        """
        Convert a node to an MObject so that it shows on the canvas
        """
        circle = Circle(radius=RADIUS).set_stroke(color=LINE_COLOR, width=WIDTH).set_fill(BACKGROUND, opacity=1.0)
        text = Text(str(self.value), color=LINE_COLOR, font=FONT, weight=BOLD, font_size=VALUE_SIZE)
        key_mobject_list = [("c", circle), ("t", text)]
        self.mobject = VDict(key_mobject_list).shift(RIGHT * self.position_x + UP * self.position_y).set_z_index(1)

    def _create_text_mobject(self, value):
        return Tex(str(value), color=LINE_COLOR).scale(FONT_SIZE)

    def highlight_stroke(self, color=GREEN):
        """
        Change the stroke color of the node to be highlight color
        """
        return self.mobject.animate.set_stroke(color=color)

    def mark_pink1(self):
        """
        Fill this node as PINK1 (dark pink)
        """
        return AnimationGroup(self.mobject["c"].animate.set_fill(PINK1).set_stroke(PINK2), self.mobject["t"].animate.set_color(BACKGROUND))

    def color(self, fill_color=PINK1, stroke_color=PINK2):
        """
        Fill this node as PINK (light pink)
        """
        return AnimationGroup(self.mobject["c"].animate.set_fill(fill_color).set_stroke(stroke_color), self.mobject["t"].animate.set_color(BACKGROUND))

    def mark_pink3(self):
        """
        Fill this node as PINK (light pink)
        """
        return AnimationGroup(self.mobject["c"].animate.set_fill(PINK3).set_stroke(PINK3), self.mobject["t"].animate.set_color(BACKGROUND))
    
    def mark_blue1(self):
        """
        Fill this node as BLUE
        """
        return AnimationGroup(self.mobject["c"].animate.set_fill(BLUE1).set_stroke(BLUE1), self.mobject["t"].animate.set_color(BACKGROUND))
    
    def mark_line_pink1(self, neighbor):
        """
        Fill a line pointing to 'neighbor' as PINK
        """
        return self.neighbor2edge[neighbor].mobject.animate.set_fill(PINK1).set_stroke(PINK1)

    def mark_line_blue1(self, neighbor):
        """
        Fill a line pointing to 'neighbor' as BLUE
        """
        return self.neighbor2edge[neighbor].mobject.animate.set_fill(BLUE1).set_stroke(BLUE1)


class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        node = GraphNode(2, 1, 1)
        self.add(node.mobject)