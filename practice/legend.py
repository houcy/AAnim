from manim import *
from style import *



class Legend:
    def __init__(self, dict, is_horizontal=False):
        """
        Dict should be from color to text, such as: {PINK1: "explored", PINK3: "finished"}
        """
        self.animation = None
        inside = VGroup()
        for feature, explanation in dict.items():
            if feature[0] == "HIGHLIGHT_ROUNDED_RECTANGLE":
                command, fill_color, stroke_color = feature
                if command == "HIGHLIGHT_ROUNDED_RECTANGLE":
                    rect = RoundedRectangle(corner_radius=0.06, height=2.2*SM_RADIUS, width=2.2*SM_RADIUS).set_fill(fill_color, 1).set_stroke(color=stroke_color)
                    text = Text(str(explanation), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE).next_to(circle, RIGHT, buff=2)
                    row = VGroup(rect, text).arrange_in_grid(rows=1, buff=LEGEND_BUFF_MICRO)
                    inside += row

            else:
                fill_color, stroke_color = feature
                circle = Circle(radius=SM_RADIUS).set_fill(fill_color, 1).set_stroke(stroke_color)
                text = Text(str(explanation), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE).next_to(circle, RIGHT, buff=2)
                row = VGroup(circle, text).arrange_in_grid(rows=1, buff=LEGEND_BUFF_MICRO)
                inside += row
        if is_horizontal:
            inside = inside.arrange_in_grid(rows=1, buff=LEGEND_BUFF_MACRO_HORIZONTAL)
        else:
            inside = inside.arrange_in_grid(cols=1, col_alignments="l", buff=LEGEND_BUFF_MACRO)
        box = SurroundingRectangle(inside, corner_radius=0, color=LINE_COLOR, stroke_width=LEGEND_STROKE_WIDTH, buff=0.2)
        self.animation = AnimationGroup(FadeIn(inside), Create(box), Wait())
        self.mobjects = VGroup(inside, box)

class Test(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        l = Legend({PINK1: "MST so far", ("HIGHLIGHT_ROUNDED_RECTANGLE", PINK1, HIGHLIGHT_STROKE): "v"})
        self.play(l.animation)