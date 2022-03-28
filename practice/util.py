from typing import Text
from manim import *
from style import *
from manim_fonts import * 

def watermark():
    return Text("Compsyc", color=PINK3, weight="BOLD", font=FONT, font_size=160).set_fill(opacity=0.03).set_z_index(100)

def show_title(text, up_mobject=None, title_scale=0.25):
    t, animation1, animation2 = None, None, None
    if not up_mobject:
        # The Title
        t = Paragraph(*text, color=GRAY, font=FONT, weight="BOLD", font_size=TITLE_SIZE)
        animation1 = Write(t)
        animation2 = t.animate.scale(title_scale).set_color(GRAY_OUT).to_edge(UL, buff=0.8).shift(0.2 * UP)
    else:
        # The secondary title
        t = Text(text, color=GRAY, font=FONT, weight="BOLD", font_size=SECONDARY_TITLE_SIZE)
        animation1 = Write(t)
        animation2 = t.animate.scale(0.5).next_to(up_mobject, DOWN, buff=0.2).align_to(up_mobject, LEFT)
    return t, animation1, animation2

def get_text(text, font_size=VALUE_SIZE, color=GRAY, weight=NORMAL):
    return Text(text, color=color, font=FONT, weight=weight, font_size=font_size)

def show_title_for_demo(text):
    title_mobject = get_text(text, font_size=TITLE_SIZE_FOR_DEMO, color=GRAY_OUT, weight=BOLD).to_edge(UL, buff=0.8).shift(0.2 * UP)
    return title_mobject

def extract_min_node(list):
    min_so_far = float('inf')
    min_node = None
    for n in list:
        if n.key < min_so_far:
            min_so_far = n.key
            min_node = n
    list.remove(min_node)
    return min_node


