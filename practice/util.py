from typing import Text
from manim import *
from style import *
from manim_fonts import * 

def watermark():
    return Text("Compsyc", color=LIGHT_PINK, weight="BOLD", font=FONT, font_size=160).set_fill(opacity=0.03).set_z_index(-100)


def get_text(text, font_size=VALUE_SIZE, color=GRAY):
    return Text(text, color=color, font=FONT, weight="BOLD", font_size=font_size)

