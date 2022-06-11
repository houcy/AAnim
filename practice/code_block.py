from manim import *
from style import *
from manim_fonts import *
from code_constant import *


class CodeBlock():
    def __init__(self, code, font=CODE_FONT):
        with RegisterFont(CODE_FONT) as fonts:
            self.code = Code(code=code, stroke_width=1, line_spacing=CODE_LINE_SPACING, font=font, background="rectangle", margin=0, background_stroke_width=0, tab_width=2, language="Python", font_size=16).shift(SHIFT_LEFT_UNIT * LEFT + SHIFT_UP_UNIT * UP)
            self.top = self.code.get_top()[1]
            self.left = self.code.get_left()[0]
            self.bottom = self.code.get_bottom()[1]
            self.right = self.code.get_right()[0]
            self.total_lines = len(self.code.code_json)
            self.height = self.top - self.bottom
            self.width = self.right - self.left
            self.line_height = self.height / (self.total_lines + self.total_lines*CODE_LINE_SPACING - CODE_LINE_SPACING)
            self.line_height_include_spacing = self.line_height + self.line_height * CODE_LINE_SPACING
            self.highlight_rect = None
            self.title = None
            self._set_background_color()
            self.last_n_lines = 1

    def _set_background_color(self):
        self.code.background_mobject.set_fill(BACKGROUND)

    def create_title(self, title):
        self.title = Text(title, color=LINE_COLOR, font="Karla").scale(TITLE_SIZE).set_z_index(2).next_to(self.code, UP, buff=0.5)
        return self.title

    def highlight(self, line_number, n_lines=1):
        """
        To highlight line 3 for example: self.play(code_instance.highlight(3))
        """
        if line_number+n_lines-1 > self.total_lines or line_number <= 0:
            print("Error: line number out of the range")
            return
        y_base = self.top - self.line_height_include_spacing * (line_number - 1) - 0.5 * self.line_height
        y_position = y_base - (n_lines - 1) * (self.line_height_include_spacing / 2)
        if not self.highlight_rect:
            self.highlight_rect = RoundedRectangle(corner_radius=0.05, width=self.width+CODE_BLOCK_WIDTH_PADDING, height=self.line_height_include_spacing*n_lines+CODE_BLOCK_HEIGHT_PADDING).set_stroke(color=GRAY, width=BOX_STROKE_WIDTH).shift(SHIFT_LEFT_UNIT * LEFT + UP * (y_position))
            self.last_n_lines = n_lines
            self.code = VGroup(self.code, self.highlight_rect)
            return AnimationGroup(FadeIn(self.highlight_rect), Wait(), lag_ratio=1)
        else:
            if self.last_n_lines == n_lines:
                return AnimationGroup(Wait(), self.highlight_rect.animate.move_to(SHIFT_LEFT_UNIT * LEFT + UP * (y_position)), Wait(), lag_ratio=1)
            else:
                self.last_n_lines = n_lines
                last_highlight_rect = self.highlight_rect
                self.highlight_rect = RoundedRectangle(corner_radius=0.05, width=self.width+CODE_BLOCK_WIDTH_PADDING, height=self.line_height_include_spacing*n_lines+CODE_BLOCK_HEIGHT_PADDING).set_stroke(color=GRAY, width=BOX_STROKE_WIDTH).shift(SHIFT_LEFT_UNIT * LEFT + UP * (y_position))
                return AnimationGroup(Wait(), ReplacementTransform(last_highlight_rect, self.highlight_rect), Wait(), lag_ratio=1)

    def if_condition(self, is_true=True, wait_time=1):
        mark = None
        if is_true:
            mark = SVGMobject("check.svg", height=0.2).set_fill(color=GREEN).next_to(self.highlight_rect, RIGHT, buff=0.2)
        else:
            mark = SVGMobject("xmark.svg", height=0.2).set_fill(color=RED).next_to(self.highlight_rect, RIGHT, buff=0.2)
        return Succession(FadeIn(mark), Wait(wait_time), FadeOut(mark), lag_ratio=1)


class Test(Scene):
    def construct(self):
        TEST_CODE = """EXTRACT-FIRST(A) {
        heapsize = length(A)
        Exchange A[1] with A[heapsize]
        }
        """
        test_code = CodeBlock(TEST_CODE)
        self.play(Create(test_code.code.shift(4*RIGHT)))
        self.play(test_code.highlight(1, 1))
        self.play(test_code.highlight(2, 1))
        self.play(test_code.highlight(4, 2))
