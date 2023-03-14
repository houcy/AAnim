from typing import Text
from manim import *
from style import *
from manim_fonts import * 
from manim import *
from style import *
from code_constant import *


def watermark():
    return Text("AAnim", color=GRAY, weight=BOLD, font=FONT, font_size=110).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100)
    
def show_title(text, up_mobject=None, title_scale=0.25, font_size=TITLE_SIZE):
    t = None
    animations = []
    if not up_mobject:
        # The Title
        t = Paragraph(*text, color=GRAY, font=FONT, weight="BOLD", font_size=font_size)
        animations = [Write(t), t.animate.scale(title_scale).set_color(GRAY_OUT).to_edge(UL, buff=0.7).shift(0.1 * UP)]
    else:
        # The secondary title
        t = Text(text, color=GRAY, font=FONT, weight="BOLD", font_size=SECONDARY_TITLE_SIZE)
        animations = [Write(t), t.animate.scale(0.5).next_to(up_mobject, DOWN, buff=0.2).align_to(up_mobject, LEFT)]
    return t, Succession(*animations)

def get_text(text, font_size=VALUE_SIZE, color=GRAY, weight=NORMAL, width=None, line_spacing=-1):
    if font_size < 40:
        return Text(text, color=color, font=FONT, weight=weight, font_size=font_size*2, line_spacing=line_spacing).scale(0.5)
    else:
        return Text(text, color=color, font=FONT, weight=weight, font_size=font_size, line_spacing=line_spacing)

def show_title_for_demo(text):
    title_mobject = get_text(text, font_size=TITLE_SIZE_FOR_DEMO*2, color=GRAY_OUT, weight=BOLD).scale(0.5).to_edge(UL, buff=0.7).shift(0.1 * UP)
    return title_mobject

def scale_position(positions, x_scale=1, y_scale=1):
    pos = {}
    for node, position in positions.items():
        x, y = position
        pos[node] = (x*x_scale, y*y_scale)
    return pos