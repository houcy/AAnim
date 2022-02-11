from manim import *
from style import *

class Legend:
    def __init__(self, dict):
        """
        Dict should be from color to text, such as: {PINK1: "explored", PINK3: "finished"}
        """
        self.animation = None
        inside = VGroup()
        for color, explanation in dict.items():
            circle = Circle(color=color, radius=SM_RADIUS).set_fill(color, opacity=1.0)
            text = Text(str(explanation), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE).next_to(circle, RIGHT, buff=2)
            inside += circle
            inside += text
        inside = inside.arrange_in_grid(cols=2, buff=LEGEND_BUFF)
        box = SurroundingRectangle(inside, color=LINE_COLOR, stroke_width=LEGEND_STROKE_WIDTH, buff=0.2)
        self.animation = AnimationGroup(FadeIn(inside), Create(box))
        self.mobjects = VGroup(inside, box)

class Test(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        l = Legend({PINK1: "curr level", PINK3: "next level", BLUE1: "finished"})
        self.play(l.animation)

            