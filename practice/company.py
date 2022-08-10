from manim import *
from manim_fonts import *
from style import *
from util import *


class Company():
    def __init__(self, name_string, character, font_size=20, color=GRAY, scale=1):
        self.name = name_string + character.name
        self.mobject = get_text(name_string, weight=ULTRAHEAVY, font_size=font_size*scale, color=color).next_to(character.mobject, UP, buff=COMPANY_CHARACTER_BUFF*scale).align_to(character.mobject, LEFT)
        self.is_showing = False
        self.scale = 1

    def fade_in(self):
        return FadeIn(self.mobject)

    def fade_out(self):
        return FadeOut(self.mobject)

    def move_to_top_right(self, scale=1):
        self.mobject.save_state()
        self.scale = self.scale * scale
        return self.mobject.animate.scale(scale).to_edge(UR, buff=0.6)

    def back_from_top_right(self):
        return Restore(self.mobject)