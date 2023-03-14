from manim import *
from style import *

LINE_WIDTH = 7

class Legend:
    def __init__(self, dict, is_horizontal=False, save_space=False):
        """
        Dict should look like this: {("LINE", fill_color, stroke_color): "description text that you want to show"}
        """
        self.animation = None
        inside = VGroup()
        self.box = None
        for feature, description in dict.items():
            type = feature[0]
            # if type == "HIGHLIGHT_ROUNDED_RECTANGLE":
            #     command, fill_color, stroke_color = feature
            #     if command == "HIGHLIGHT_ROUNDED_RECTANGLE":
            #         rect = RoundedRectangle(corner_radius=0.06, height=2.2*SM_RADIUS, width=2.2*SM_RADIUS).set_fill(fill_color, 1).set_stroke(color=stroke_color)
            #         text = Text(str(explanation), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE*2).scale(0.5).next_to(circle, RIGHT, buff=2)
            #         if is_horizontal or save_space:
            #             row = VGroup(rect, text).arrange_in_grid(rows=1, buff=LEGEND_BUFF_MICRO)
            #             inside += row
            #         else:
            #             inside += rect
            #             inside += text
            if type == "MULTICOLORS":
                legend = VGroup()
                if feature[1] == "CIRCLE":
                    for i, color in enumerate(MULTI_COLORS):
                        legend += Circle(radius=SM_RADIUS).set_fill(color, 1).set_stroke(color).shift((i * SM_RADIUS*1.5) * RIGHT)
                elif feature[1] == "LINE":
                    for i, color in enumerate(MULTI_COLORS):
                        legend += Line(start=[0, 0, 0], end=[0.21, 0, 0]).set_fill(color, 1).set_stroke(color, width=LINE_WIDTH).shift((i * 0.1) * DOWN)
                text = Text(str(description), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE).next_to(legend, RIGHT, buff=2)
                if is_horizontal or save_space:
                    row = VGroup(legend, text).arrange_in_grid(rows=1, buff=LEGEND_BUFF_MICRO)
                    inside += row
                else:
                    inside += legend
                    inside += text
            elif type == "LINE":
                _, fill_color, stroke_color = feature
                line = Line(start=[0, 0, 0], end=[0.21, 0, 0]).set_fill(fill_color, 1).set_stroke(stroke_color, width=LINE_WIDTH)
                text = Text(str(description), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE*2).scale(0.5).next_to(line, RIGHT, buff=2)
                if is_horizontal or save_space:
                    row = VGroup(line, text).arrange_in_grid(rows=1, buff=LEGEND_BUFF_MICRO)
                    inside += row
                else:
                    inside += line
                    inside += text
            elif type == "CIRCLE":
                _, fill_color, stroke_color = feature
                circle = Circle(radius=SM_RADIUS).set_fill(fill_color, 1).set_stroke(stroke_color)
                text = Text(str(description), color=LINE_COLOR, font=FONT, font_size=LEGEND_SIZE*2).scale(0.5).next_to(circle, RIGHT, buff=2)
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
        self.animation = AnimationGroup(FadeIn(inside), Create(box))
        self.mobjects = VGroup(inside, box)
        self.inside = inside
        self.box = box

    def fade_in(self):
        return AnimationGroup(FadeIn(self.inside), Create(self.box))

    def fade_out(self):
        return FadeOut(self.mobjects)

    def next_to(self, mobject, direction=UP, buff=LEGEND_CHARACTER_BUFF):
        return self.mobjects.animate.next_to(mobject, direction, buff=buff)

    def next_to_character_top_left(self, mobject, direction=LEFT, buff=LEGEND_CHARACTER_BUFF):
        return self.mobjects.animate.next_to(mobject, direction, buff=buff)

class Test(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        l = Legend({PINK1: "MST so far", ("HIGHLIGHT_ROUNDED_RECTANGLE", PINK1, HIGHLIGHT_STROKE): "v"})
        self.play(l.animation)