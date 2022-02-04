from manim import *
from style import *


class GraphNode:
    def __init__(self, value, position_x, position_y):
        self.value = value
        self.neighbor2line = {}
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
        text = Tex(str(self.value), color=LINE_COLOR).scale(FONT_SIZE)
        key_mobject_list = [("c", circle), ("t", text)]
        self.mobject = VDict(key_mobject_list).shift(RIGHT * self.position_x + UP * self.position_y).set_z_index(1)

    def _create_text_mobject(self, value):
        return Tex(str(value), color=LINE_COLOR).scale(FONT_SIZE)

    def mark_discovered(self):
        return AnimationGroup(self.mobject["c"].animate.set_fill(PINK3).set_stroke(PINK3), self.mobject["t"].animate.set_color(BACKGROUND))
    
    def mark_finished(self):
        return AnimationGroup(self.mobject["c"].animate.set_fill(PINK1).set_stroke(PINK1), self.mobject["t"].animate.set_color(BACKGROUND))

# class Test(Scene):
#     def construct(self):
#         self.camera.background_color = BACKGROUND
#         node = HeapNode(2, 1, 1)
#         self.add(node.mobject)