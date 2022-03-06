from manim import *
from manim_fonts import *
from style import *
from util import *


class GraphNode:
    def __init__(self, value, position_x, position_y):
        self.value = value
        self.neighbor2edge = {}
        self.edges = []
        self.position_x = position_x
        self.position_y = position_y
        self.mobject = None
        self.text_mobject = None
        self._create_mobject()
        self.key = None
        self.key_mobject = None
    
    def _create_mobject(self):
        """
        Convert a node to an MObject so that it shows on the canvas
        """
        circle = Circle(radius=RADIUS).set_stroke(color=LINE_COLOR, width=WIDTH).set_fill(BACKGROUND, opacity=1.0)
        self.text_mobject = Text(str(self.value), color=LINE_COLOR, font=FONT, weight=BOLD, font_size=VALUE_SIZE)
        key_mobject_list = [("c", circle), ("t", self.text_mobject)]
        self.mobject = VDict(key_mobject_list).shift(RIGHT * self.position_x + UP * self.position_y).set_z_index(1)

    def change_key(self, key):
        animations = []
        if not self.key:
            self.key = key
            new_text_mobject = get_text(str(self.value), NODE_NAME_BACKGROUND_SIZE).move_to(self.mobject.get_center()).set_fill(opacity=NODE_NAME_BACKGROUND_OPACITY)
            animations.append(Transform(self.text_mobject, new_text_mobject))
            self.text_mobject = new_text_mobject
            animations.append(Wait(2))
            self.key_mobject = get_text(str(self.key), font_size=VALUE_SIZE).move_to(self.mobject.get_center()).set_z_index(2)
            self.mobject["key"] = self.key_mobject
            animations.append(FadeIn(self.key_mobject))
        else:
            new_key_mobject = get_text(str(key), font_size=VALUE_SIZE).move_to(self.mobject.get_center()).set_z_index(2)
            animations.append(Transform(self.key_mobject, new_key_mobject))
            self.key = key
            self.key_mobject = new_key_mobject
        return AnimationGroup(*animations, lag_ratios=1)


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
        node = GraphNode(value='A', position_x=1, position_y=1)
        self.add(node.mobject)
        self.play(node.change_key(3))
        self.play(node.change_key(5))