from manim import *
from manim_fonts import *
from style import *
from util import *

BUFF_PADDING = 0.3

class LeftSideOutline():
    def __init__(self, string, buff=1):
        self.string2mobject = {}
        self.buff = buff
        self.string2mobject[string] = self._get_text(string)
        self.strings = []
        self.strings.append(string)
        # self.height = self.string2mobject[string].get_bottom() - self.string2mobject[string].get_top()

    def _get_text(self, string, weight=BOLD, font_size=25):
        return get_text(string, weight=weight, font_size=font_size, line_spacing=0.7).to_edge(LEFT, buff=self.buff)

    def show(self, string):
        if string in self.string2mobject:
            return Write(self.string2mobject[string])
    
    def add(self, string, is_secondary=False):
        current_strings = VGroup(*list(self.string2mobject.values()))
        last_string = self.strings[-1]
        last_mobject = self.string2mobject[last_string]
        current_mobject = None
        if is_secondary:
            current_mobject = self._get_text(string, weight=NORMAL, font_size=23).next_to(last_mobject, DOWN, buff=BUFF_PADDING).align_to(last_mobject, LEFT).shift(0.4*RIGHT)
        if not is_secondary:
            current_mobject = self._get_text(string, weight=BOLD, font_size=25).next_to(last_mobject, DOWN, buff=BUFF_PADDING).align_to(last_mobject, LEFT)
        self.string2mobject[string] = current_mobject
        self.strings.append(string)
        # shift half of the new mobject's height in order to center the resulting whole outline
        half_height = (current_mobject.get_top() - current_mobject.get_bottom() + BUFF_PADDING) / 2
        animations = []
        animations.append(current_strings.animate.shift(half_height*UP))
        self.string2mobject[string].shift(half_height*UP)
        animations.append(Write(current_mobject))
        return Succession(*animations, lag_ratio=1)

    def fade_out(self):
        return FadeOut(*list(self.string2mobject.values()))