from manim import *
from manim_fonts import *
from style import *
from util import *

# z_index: edge: 0, circle: 1, text: 3, key: 5
class GraphNode:
    def __init__(self, value, position_x, position_y):
        self.value = value
        self.neighbor2edge = {}
        self.neighbors = []
        self.edges = []
        self.position_x = position_x
        self.position_y = position_y
        self.mobject = None
        self.text_mobject = None
        self.circle_mobject = None
        self._create_mobject()
        self.key = None
        self.key_mobject = None
        self.animations = None
        self.rect = None
    
    def _create_mobject(self):
        """
        Convert a node to an MObject so that it shows on the canvas
        """
        self.circle_mobject = Circle(radius=RADIUS).set_stroke(color=LINE_COLOR, width=WIDTH).set_fill(BACKGROUND, opacity=1.0).set_z_index(1)
        self.text_mobject = Text(str(self.value), color=LINE_COLOR, font=FONT, weight=BOLD, font_size=VALUE_SIZE).set_z_index(3)
        key_mobject_list = [("c", self.circle_mobject), ("t", self.text_mobject)]
        self.mobject = VDict(key_mobject_list).shift(RIGHT * self.position_x + UP * self.position_y)

    def mobjects(self):
        mobjects = VGroup()
        for m in [self.circle_mobject, self.text_mobject. self.key_mobject]:
            if m:
                mobjects += m
        return mobjects

    def initialize_key(self, key, show_value=True):
        animations = []
        key_string = ''
        if key == float('inf'):
            key_string = '∞'
        elif isinstance(key, int):
            key_string = str(key)
        else:
            print("Failed to initialize key: need passing an integer")
            return
        self.key = key
        if show_value:
            new_text_mobject = get_text(str(self.value), NODE_NAME_BACKGROUND_SIZE, color=NODE_NAME_BACKGROUND_COLOR, weight=NODE_NAME_BACKGROUND_WEIGHT).move_to(self.mobject.get_center()).set_fill(opacity=NODE_NAME_BACKGROUND_OPACITY).set_z_index(3)
            animations.append(ReplacementTransform(self.text_mobject, new_text_mobject))
            self.text_mobject = new_text_mobject
            self.mobject["t"] = new_text_mobject
        else:
            animations.append(FadeOut(self.text_mobject))
            self.mobject.remove("t")
        self.key_mobject = get_text(key_string, font_size=VALUE_SIZE, weight=BOLD).move_to(self.mobject.get_center()).set_z_index(5)
        animations.append(FadeIn(self.key_mobject))
        self.animations = animations    # 2 animations: Transform and FadeIn
        return AnimationGroup(*animations, lag_ratios=1)
    
    def update_key(self, key):
        animations = []
        new_key_mobject = get_text(str(key), font_size=VALUE_SIZE, weight=BOLD).move_to(self.mobject.get_center()).set_z_index(5)
        animations.append(ReplacementTransform(self.key_mobject, new_key_mobject))
        self.key = key
        self.key_mobject = new_key_mobject
        self.animations = animations
        return AnimationGroup(*animations, lag_ratios=1)

    def highlight_stroke(self, color=HIGHLIGHT_STROKE):
        """
        Change the stroke color of the node to be highlight color
        """
        return AnimationGroup(self.mobject.animate.set_stroke(color=color), Wait())

    def highlight_stroke_and_change_shape(self, color=HIGHLIGHT_STROKE):
        """
        Change the stroke color of the node to be highlight color
        """
        circle = self.mobject["c"]
        circle.save_state()
        circle_color = circle.get_fill_color()
        self.rect = RoundedRectangle(corner_radius=0.2, height=1.8*RADIUS, width=1.8*RADIUS).set_fill(circle_color, 1).set_stroke(color=color).move_to(circle.get_center()).set_z_index(1)
        return AnimationGroup(ReplacementTransform(circle, self.rect), Wait())

    def dehighlight_stroke_and_change_shape(self):
        """
        Change the stroke color of the node to be highlight color
        """
        return AnimationGroup(Wait(), FadeOut(self.rect), Restore(self.mobject["c"]), Wait())

    def mark_pink1(self):
        """
        Fill this node as PINK1 (dark pink)
        """
        return AnimationGroup(self.mobject["c"].animate.set_fill(PINK1).set_stroke(PINK2), self.mobject["t"].animate.set_color(BACKGROUND))

    def color(self, fill_color=PINK1, stroke_color=PINK2, has_key=False):
        """
        Fill this node as PINK (light pink)
        """
        if not has_key:
            return AnimationGroup(self.mobject["c"].animate.set_fill(fill_color).set_stroke(stroke_color), self.key_mobject.animate.set_color(BACKGROUND))
        elif "t" in self.mobject:
            return AnimationGroup(self.mobject["c"].animate.set_fill(fill_color).set_stroke(stroke_color), self.key_mobject.animate.set_color(BACKGROUND), self.mobject["t"].animate.set_color(BACKGROUND))
        else:
            return AnimationGroup(self.mobject["c"].animate.set_fill(fill_color).set_stroke(stroke_color), self.key_mobject.animate.set_color(BACKGROUND))

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