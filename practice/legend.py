from manim import *
from style import *


class Legend:
    def __init__(self, dict, is_horizontal=False, save_space=False):
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
                    text = Text(str(explanation), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE*2).scale(0.5).next_to(circle, RIGHT, buff=2)
                    if is_horizontal or save_space:
                        row = VGroup(rect, text).arrange_in_grid(rows=1, buff=LEGEND_BUFF_MICRO)
                        inside += row
                    else:
                        inside += rect
                        inside += text
            elif feature[0] == "MULTICOLORS":
                if feature[1] == "CIRCLE":
                    circles = VGroup()
                    for i, color in enumerate(MULTI_COLORS):
                        circles += Circle(radius=SM_RADIUS).set_fill(color, 1).set_stroke(color).shift((i * SM_RADIUS*1.5) * RIGHT)
                    text = Text(str(explanation), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE).next_to(circles, RIGHT, buff=2)
                    if is_horizontal or save_space:
                        row = VGroup(circles, text).arrange_in_grid(rows=1, buff=LEGEND_BUFF_MICRO)
                        inside += row
                    else:
                        inside += circles
                        inside += text
            else:
                fill_color, stroke_color = feature
                circle = Circle(radius=SM_RADIUS).set_fill(fill_color, 1).set_stroke(stroke_color)
                text = Text(str(explanation), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE*2).scale(0.5).next_to(circle, RIGHT, buff=2)
                if is_horizontal or save_space:
                    row = VGroup(circle, text).arrange_in_grid(rows=1, buff=LEGEND_BUFF_MICRO)
                    inside += row
                else:
                    inside += circle
                    inside += text
        if is_horizontal:
            inside = inside.arrange_in_grid(rows=1, buff=LEGEND_BUFF_MACRO_HORIZONTAL)
        elif save_space:
            inside = inside.arrange_in_grid(cols=1, col_alignments="l", buff=LEGEND_BUFF_MACRO)
        else:
            inside = inside.arrange_in_grid(cols=2, col_alignments=["l", "l"], buff=LEGEND_BUFF_MACRO)
        box = SurroundingRectangle(inside, corner_radius=0, color=LINE_COLOR, stroke_width=LEGEND_STROKE_WIDTH, buff=0.2)
        self.animation = AnimationGroup(FadeIn(inside), Create(box), Wait())
        self.mobjects = VGroup(inside, box)

class Test(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        l = Legend({PINK1: "MST so far", ("HIGHLIGHT_ROUNDED_RECTANGLE", PINK1, HIGHLIGHT_STROKE): "v"})
        self.play(l.animation)