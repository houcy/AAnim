from manim import *
from style import *
from util import *

class Iterator:
    def __init__(self, input):
        # string = ""
        # if isinstance(input, str):
        #     string = '"' + input + '"'
        # elif isinstance(input, list):
        #     string = '[' + "".join(input) + ']'
        self.mobject = None
        self.x_offset = 0
        self.y_offset = 0
        text_mobject = {}
        for index, ch in enumerate(input):
            text_mobject[index] = get_text(ch, font_size=M_VALUE_SIZE)
        # self.mobject = VDict(text_mobject).arrange(buff=0.5)
        x1, _, _ = self.mobject.get_left()
        x2, _, _ = self.mobject.get_right()
        width = x2 - x1
        single_width = width / len(input)
        half_single_width = single_width / 2

    def show(self):
        return VDict(text_mobject).arrange(buff=0.5)

    def initial_arrow(self):
        arrow = Arrow(start=0.6*DOWN, end=0.6*UP, color=PINK1)
        return FadeIn(arrow)

    def move_to(self, x_offset, y_offset):
        self.x_offset += x_offset
        self.y_offset += y_offset

    def next(self):
        pass


class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        i = Iterator("FDTHDKHD")
        self.play(i.first())
        self.play(i.show())