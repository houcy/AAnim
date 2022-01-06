from manim import *
from style import *

class CodeBlock():
    def __init__(self, code):
        self.code = Code(code=code, line_spacing=1, background="rectangle", margin=0, background_stroke_width=0, tab_width=2, language="Python", font="Monospace", font_size=16).shift(SHIFT_LEFT_UNIT * LEFT)
        self.top = self.code.get_top()[1]
        self.left = self.code.get_left()[0]
        self.bottom = self.code.get_bottom()[1]
        self.right = self.code.get_right()[0]
        self.total_lines = len(self.code.code_json)
        self.height = self.top - self.bottom
        self.width = self.right - self.left
        self.line_height = self.height / self.total_lines
        self.highlight_rect = None
        self.title = None

    def create_title(self, title):
        self.title = Tex(title, color=LINE_COLOR).scale(TITLE_SIZE).set_z_index(2).next_to(self.code, UP, buff=0.5)
        return self.title

    def highlight(self, line_number):
        if line_number > self.total_lines:
            return
        y_position = self.top - (line_number-0.5) * self.line_height
        if not self.highlight_rect:
            self.highlight_rect = Rectangle(width=self.width+CODE_BLOCK_RECTANGLE_WIDTH, height=self.line_height+CODE_BLOCK_RECTANGLE_HEIGHT).set_stroke(color=YELLOW, width=2).shift(SHIFT_LEFT_UNIT * LEFT + UP * y_position)
            return FadeIn(self.highlight_rect)
        else:
            return self.highlight_rect.animate.move_to(SHIFT_LEFT_UNIT * LEFT + UP * y_position)
