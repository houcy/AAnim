from manim import *
from style import *

TEST_CODE = """EXTRACT-FIRST(A) {
    heapsize = length(A)
    Exchange A[1] with A[heapsize]
    Remove A[heapsize]
    HeapifyDown(A, 1)
    heapsize = length(A)
    Exchange A[1] with A[heapsize]
    Remove A[heapsize]
    HeapifyDown(A, 1)
    heapsize = length(A)
    Exchange A[1] with A[heapsize]
    Remove A[heapsize]
    HeapifyDown(A, 1)
}
"""

CODE_FOR_BUILD = """BUILD-HEAP(A[1,...,n]) {
    for i = floor(n/2) downto 1
        HeapifyDown(A, i)
}
"""

CODE_LINE_SPACING = 1

class CodeBlock():
    """
    To highlight line 3 for example: self.play(code_instance.highlight(3))
    """
    def __init__(self, code):
        self.code = Code(code=code, line_spacing=CODE_LINE_SPACING, background="rectangle", margin=0, background_stroke_width=0, tab_width=2, language="Python", font="Monospace", font_size=16).shift(SHIFT_LEFT_UNIT * LEFT)
        self.top = self.code.get_top()[1]
        self.left = self.code.get_left()[0]
        self.bottom = self.code.get_bottom()[1]
        self.right = self.code.get_right()[0]
        self.total_lines = len(self.code.code_json)
        self.height = self.top - self.bottom
        self.width = self.right - self.left
        self.line_height = self.height / (self.total_lines + self.total_lines*CODE_LINE_SPACING - CODE_LINE_SPACING)
        self.highlight_rect = None
        self.title = None
        self._set_background_color()

    def _set_background_color(self):
        self.code.background_mobject.set_fill(BACKGROUND_COLOR)

    def create_title(self, title):
        self.title = Tex(title, color=LINE_COLOR).scale(TITLE_SIZE).set_z_index(2).next_to(self.code, UP, buff=0.5)
        return self.title

    def highlight(self, line_number):
        if line_number > self.total_lines or line_number <= 0:
            print("Error: line number out of the range")
            return
        y_position = self.top - (self.line_height + self.line_height * CODE_LINE_SPACING) * (line_number - 1) - 0.5 * self.line_height
        if not self.highlight_rect:
            self.highlight_rect = Rectangle(width=self.width+CODE_BLOCK_WIDTH_PADDING, height=self.line_height+CODE_BLOCK_HEIGHT_PADDING).set_stroke(color=HIGHLIGHT_COLOR, width=2).shift(SHIFT_LEFT_UNIT * LEFT + UP * y_position)
            return FadeIn(self.highlight_rect)
        else:
            return self.highlight_rect.animate.move_to(SHIFT_LEFT_UNIT * LEFT + UP * y_position)


class CodeScene(Scene):
    def construct(self):
        code2 = CodeBlock(CODE_FOR_BUILD)
        self.play(FadeIn(code2.code))
        for i in range(1, 4):
            self.play(code2.highlight(i))