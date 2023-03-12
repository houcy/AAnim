from manim import *
from style import *
from manim_fonts import *
from code_constant import *


class CodeBlock():
    def __init__(self, code, font=CODE_FONT):
        with RegisterFont(CODE_FONT) as fonts:
            self.code = Code(code=code, stroke_width=1, line_spacing=CODE_LINE_SPACING, font=font, background="rectangle", margin=0, background_stroke_width=0, tab_width=2, language="Python", font_size=16)
            self.top = self.code.get_top()[1]
            self.left = self.code.get_left()[0]
            self.bottom = self.code.get_bottom()[1]
            self.right = self.code.get_right()[0]
            self.total_lines = len(self.code.code_json)
            self.height = self.top - self.bottom
            self.width = self.right - self.left
            self.line_height = self.height / (self.total_lines + self.total_lines*CODE_LINE_SPACING - CODE_LINE_SPACING)
            self.spacing = self.line_height * CODE_LINE_SPACING
            self.line_height_include_spacing = self.line_height + self.spacing
            self.highlight_rect = None
            self.title = None
            self._set_background_color(self.code)
            self.last_n_lines = 1
            self.x_offset = 0
            self.y_offset = 0

    def _set_background_color(self, code_mobject):
        code_mobject.background_mobject.set_fill(BACKGROUND)

    def create_title(self, title):
        self.title = Text(title, color=LINE_COLOR, font="Karla").scale(TITLE_SIZE).set_z_index(2).next_to(self.code, UP, buff=0.5)
        return self.title

    def create(self, x_offset=0, y_offset=0):
        self.x_offset = x_offset
        self.y_offset = y_offset
        return Create(self.code.shift(self.x_offset * RIGHT + self.y_offset * UP))

    def shift(self, x_offset=0, y_offset=0):
        self.x_offset += x_offset
        self.y_offset += y_offset
        return self.code.animate.shift(self.x_offset * RIGHT + self.y_offset * UP)

    def shift_only(self, x_offset=0, y_offset=0):
        self.x_offset += x_offset
        self.y_offset += y_offset
        self.code.shift(self.x_offset * RIGHT + self.y_offset * UP)

    def fade_out(self):
        if self.highlight_rect:
            return FadeOut(self.code, self.highlight_rect)
        else:
            return FadeOut(self.code)

    def highlight(self, line_number, n_lines=1, wait_time_before=1, wait_time_after=1, character_object=None, company=''):
        """
        To highlight line 3 for example: self.play(code_instance.highlight(3))
        character_object is only for making videos about fairytales
        """
        if line_number+n_lines-1 > self.total_lines or line_number <= 0:
            print("Error: line number out of the range")
            return
        y_base = self.top - self.line_height_include_spacing * (line_number - 1) - 0.5 * self.line_height
        y_position = y_base - (n_lines - 1) * (self.line_height_include_spacing / 2)
        animations = [Wait(wait_time_before)]
        rect_width = 0
        if self.total_lines < 10:
            rect_width = self.width+CODE_BLOCK_WIDTH_PADDING
        else:
            rect_width = self.width+CODE_BLOCK_WIDTH_PADDING-0.1    # When total_lines >= 10, the padding will be larger
        if not self.highlight_rect:
            # Create a rect
            self.highlight_rect = RoundedRectangle(corner_radius=0.05, width=rect_width, height=self.line_height_include_spacing*n_lines+CODE_BLOCK_HEIGHT_PADDING).set_stroke(color=GRAY, width=BOX_STROKE_WIDTH).shift(self.x_offset * RIGHT + (y_position + self.y_offset) * UP)
            self.last_n_lines = n_lines
            # self.code = VGroup(self.code, self.highlight_rect)
            if character_object and company:
                # character_object is only for making videos about fairytales, appear together with the rect
                animations.append(AnimationGroup(FadeIn(self.highlight_rect), character_object.highlight(company)))
            else:
                animations.append(FadeIn(self.highlight_rect))
            animations.append(Wait(wait_time_after))
            return Succession(*animations, lag_ratio=1)
        else:
            if self.last_n_lines == n_lines:
                # No change on rect
                if character_object and company:
                    animations.append(AnimationGroup(self.highlight_rect.animate.move_to(self.x_offset * RIGHT + (y_position + self.y_offset) * UP), character_object.highlight(company)))
                else:
                    animations.append(self.highlight_rect.animate.move_to(self.x_offset * RIGHT + (y_position + self.y_offset) * UP))
            else:
                # Change the height of the rect
                self.last_n_lines = n_lines
                last_highlight_rect = self.highlight_rect
                self.highlight_rect = RoundedRectangle(corner_radius=0.05, width=rect_width, height=self.line_height_include_spacing*n_lines+CODE_BLOCK_HEIGHT_PADDING).set_stroke(color=GRAY, width=BOX_STROKE_WIDTH).shift(self.x_offset * RIGHT + (y_position + self.y_offset) * UP)
                if character_object and company:
                    animations.append(AnimationGroup(ReplacementTransform(last_highlight_rect, self.highlight_rect), character_object.highlight(company)))
                else:
                    animations.append(ReplacementTransform(last_highlight_rect, self.highlight_rect))
            animations.append(Wait(wait_time_after))
            return Succession(*animations, lag_ratio=1)

    def dehighlight_character(self, character):
        return character.dehighlight()
    
    def destroy_highlight(self):
        if self.highlight_rect:
            self.highlight_rect = None
            return FadeOut(self.highlight_rect)

    def if_true(self, is_true=True, wait_time=1):
        """
        How to use:
        self.play(code_block.if_true(wait_time=4))
        self.play(code_block.if_true(is_true=False, wait_time=4))
        """
        # mark = None
        # if is_true:
        #     mark = SVGMobject("check.svg", height=0.17).set_fill(color=GREEN)
        # else:
        #     mark = SVGMobject("xmark.svg", height=0.17).set_fill(color=RED)
        # mark.align_to(self.highlight_rect, UL).shift(CONDITION_MARK_SHIFT_RIGHT_UNIT*RIGHT+0.09*DOWN)
        # return Succession(FadeIn(mark), Wait(wait_time), FadeOut(mark), lag_ratio=1)
        
        mark = None
        if is_true:
            mark = SVGMobject("check.svg", height=0.17).set_fill(color=GREEN).set_z_index(8)
        else:
            mark = SVGMobject("xmark.svg", height=0.17).set_fill(color=RED).set_z_index(8)
        mark_background = RoundedRectangle(corner_radius=0.05, width=0.4, height=0.28).set_fill(BACKGROUND, opacity=0.9).set_stroke(width=0).set_z_index(6)
        mark_group = VGroup(mark, mark_background)
        mark_group.move_to(self.highlight_rect).align_to(self.highlight_rect, UR).shift(0.03*LEFT, 0.03*DOWN)
        return Succession(FadeIn(mark_group), Wait(wait_time), FadeOut(mark_group), lag_ratio=1)


    def replace(self, line_no_from, replacement_code, font=CODE_FONT):
        # The replacement code replace all lines starting from the line_no_from ending at the last line. It can't be an insertion.
        # Replace the bottom part
        replacement_code_mobject = Code(code=replacement_code, stroke_width=1, line_spacing=CODE_LINE_SPACING, font=font, background="rectangle", margin=0, background_stroke_width=0, tab_width=2, language="Python", font_size=16, line_no_from=line_no_from)
        self._set_background_color(replacement_code_mobject)
        replacement_code_mobject.align_to(self.code, LEFT).align_to(self.code, UP)
        replacement_code_mobject.shift((line_no_from-1) * self.line_height_include_spacing * DOWN)
        # Create a rectangle to hide the bottom part
        rect_height = (self.total_lines-line_no_from+1) * self.line_height_include_spacing
        rect = Rectangle(color=BACKGROUND, height=rect_height, width=self.width).set_fill(BACKGROUND, opacity=1).align_to(self.code, LEFT).align_to(self.code, UP)
        rect.shift((line_no_from-1) * self.line_height_include_spacing * DOWN).shift(self.spacing / 2 * UP)
        # Update attributes
        replacement_number_lines = len(replacement_code_mobject.code_json)
        self.total_lines = line_no_from + replacement_number_lines - 1
        self.bottom = replacement_code_mobject.get_bottom()[1]
        self.height = self.top - self.bottom
        self.code = VGroup(self.code, replacement_code_mobject)
        return AnimationGroup(FadeIn(rect), FadeIn(replacement_code_mobject))

    # def shift(self, x_offset, y_offset)



class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        test_code = CodeBlock(CODE_FOR_DIJKASTRA_WITHOUT_RELAX)
        self.play(test_code.create(-2.9, -0.2))
        self.play(test_code.replace(9, """              RELAX(u, v, weight)
}

RELAX(u, v, weight) {
    if v.key > u.key + weight(u, v)
        v.key = u.key + weight(u, v)
        v.previous = u
}
"""))

        # test_code2 = CodeBlock(CODE_FOR_RELAX)
        # self.play(test_code2.create())
        # self.play(test_code.highlight(1, 1))
        # self.play(test_code.highlight(5, 1))
        # self.play(test_code.if_true(False))
        # self.play(test_code.if_true())
        # self.play(test_code.highlight(3, 1))
        # self.play(test_code.if_true())
        # self.play(test_code.highlight(4, 2))
        # self.play(test_code.if_true(False))
        # self.play(test_code.if_true())
        # self.play(test_code.if_true())
        # self.play(test_code.fade_out())
        # self.wait()

        # test_code = CodeBlock(CODE_FOR_PRIM_BASIC)
        # self.play(test_code.create(x_offset=-2, y_offset=2))
        # self.play(test_code.highlight(1, 1))
        # self.play(test_code.highlight(2, 1))
        # self.play(test_code.if_true(False))
        # self.play(test_code.highlight(3, 1))
        # self.play(test_code.if_true())
        # self.play(test_code.highlight(4, 2))
        # self.play(test_code.if_true())
        # self.play(test_code.fade_out())
        # self.wait()