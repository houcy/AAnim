from manim import *
from manim_fonts import *
from style import *
from util import *


class Company():
    def __init__(self, name_string, character, font_size=COMPANY_FONT_SIZE_TOP_RIGHT, color=GRAY, scale=1):
        self.name = name_string + character.name
        self.mobject = get_text(name_string, weight=ULTRAHEAVY, font_size=font_size*scale, color=color).next_to(character.mobject, UP, buff=COMPANY_CHARACTER_BUFF*scale).align_to(character.mobject, LEFT)
        self.is_showing = False
        self.scale = 1
        self.scale_time = 1 # Only used for top right scaling

    def fade_in(self):
        return FadeIn(self.mobject)

    def fade_out(self):
        return FadeOut(self.mobject)

    def move_to_top_right(self):
        self.mobject.save_state()
        scale_time = COMPANY_FONT_SIZE_TOP_RIGHT / self.mobject.font_size
        return self.mobject.animate.scale(scale_time).to_edge(UR, buff=0.6)

    def back_from_top_right(self):
        return Restore(self.mobject)

    def shift(self, x_offset=0, y_offset=0, scale=1):
        self.scale = self.scale * scale
        return self.mobject.animate.scale(scale).shift(x_offset * RIGHT + y_offset * UP)

    def next_to(self, object, direction, buff=0, scale=1):
        self.scale = self.scale * scale
        return self.mobject.animate.scale(scale).next_to(object.mobject, direction, buff=buff)

    def move_to(self, x_offset=0, y_offset=0):
        return self.mobject.animate.move_to(x_offset * RIGHT + y_offset * UP)