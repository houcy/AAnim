from manim import *
from style import *


class TableLine:
    def __init__(self, array, is_mobject=False, buff=0.5, show_box=True, x_position=0, y_position=0):
        """
        Parameter
        1. array: a list of content(int or str)
        2. buff: the distance between the first line and the second line
        """
        self.animation = None
        self.buff = buff
        self.is_mobject = is_mobject
        self.text2index = {} # A dict from the Tex mobject to its index in VDict
        self.index2square = {} # A dict that is up to 15 elements
        self.mobject = None # A VDict of all squres and text
        self.need_update_mobject = False
        self.empty_mobject = None
        self.show_box = show_box
        self.current_index_scan = None
        self.highlight_rect = None
        self.create_highlight_rec_animation = None
        self.x_position = x_position
        self.y_position = y_position
        if len(array) >= 15:
            print("Array is too long")
            return
        if len(array) == 0:
            return
        if is_mobject:
            index = 0
            for mob in array:
                square = VDict([("box", Square(side_length=TABLE_SIDE_LENGTH, stroke_color=GRAY)), ("text", mob)])
                if not show_box:
                    square.set_stroke(BACKGROUND)
                self.text2index[mob] = index
                self.index2square[index] = square
                index += 1
        else:
            for index, value in enumerate(array):
                text_mobject = self._create_text_mobject(value)
                self.text2index[text_mobject] = index
                square = VDict([("box", Square(side_length=TABLE_SIDE_LENGTH, stroke_color=GRAY)), ("text", text_mobject)])
                if not show_box:
                    square.set_stroke(BACKGROUND)
                self.index2square[index] = square
        self._update_table_line_mobject()
        animations = []
        for index in range(16):
            if index in self.index2square:
                square = self.index2square[index]
                animations.append(FadeIn(square))
        self.animation = AnimationGroup(*animations, lag_ratios=0.5)

    def _update_table_line_mobject(self):
        self.mobject = VDict(self.index2square).arrange(buff=0).move_to(self.x_position*RIGHT + self.y_position*UP)

    def _create_text_mobject(self, value):
        return Text(str(value), color=LINE_COLOR, font=FONT, weight="BOLD", font_size=VALUE_SIZE)

    def _move_to_origin(self):
        position_y = self.mobject.get_y()
        return self.mobject.animate.move_to([0, position_y, 0])

    def _show_empty_text(self):
        self.empty_mobject = self._create_text_mobject("I'm empty")
        return FadeIn(self.empty_mobject)

    def _remove_empty_text(self, animations):
        animations.append(FadeOut(self.empty_mobject))
        self.empty_mobject = None
        return animations

    def length(self):
        return len(self.index2square)

    def show(self):
        if self.animation:
            return self.animation
        else:
            return self._show_empty_text()

    def initialize_scan(self, index=0):
        self.current_index_scan = index
        if self.need_update_mobject:
            self._update_table_line_mobject()
        current_mobject = self.index2square[self.current_index_scan]
        self.highlight_rect = Square(side_length=TABLE_SIDE_LENGTH, stroke_color=GRAY).move_to(current_mobject.get_center())
        self.create_highlight_rec_animation = Create(self.highlight_rect)

    def scan_next(self, next_index=None):
        if self.create_highlight_rec_animation:
            temp = self.create_highlight_rec_animation
            self.create_highlight_rec_animation = None
            return temp
        if (not next_index and self.current_index_scan == self.length() - 1) or (next_index and next_index >= self.length()):
            return FadeOut(self.highlight_rect)
        elif next_index:
            index_offset = next_index - self.current_index_scan
            self.current_index_scan = next_index
            return self.highlight_rect.animate.shift(index_offset * TABLE_SIDE_LENGTH * RIGHT)
        else:
            self.current_index_scan += 1
            return self.highlight_rect.animate.shift(TABLE_SIDE_LENGTH* RIGHT)

    def get_mobject(self):
        if self.need_update_mobject:
            self._update_table_line_mobject()
        return self.mobject

    def add(self, element):
        if self.need_update_mobject:
            self._update_table_line_mobject()
        animations = []
        text_mobject = None
        if self.is_mobject:
            text_mobject = element
        else:
            text_mobject = self._create_text_mobject(element)
        square = VDict([("box", Square(side_length=TABLE_SIDE_LENGTH)), ("text", text_mobject)])
        if not self.show_box:
            square.set_stroke(BACKGROUND)
        index = self.length()
        if index != 0:
            square.next_to(self.mobject, RIGHT, buff=0)
            self.mobject = self.mobject.add([(index, square)])
        else:
            animations = self._remove_empty_text(animations)
            self.mobject = VDict({0: square})
        animations.append(FadeIn(square))
        animations.append(self._move_to_origin())
        self.animation = AnimationGroup(*animations)
        self.text2index[text_mobject] = index
        self.index2square[index] = square
        return self.animation

    def remove_last(self):
        if self.need_update_mobject:
            self._update_table_line_mobject()
        if self.length() == 0:
            print("Array is empty")
            return
        last_index = self.length() - 1
        animations = []
        last_square = self.mobject[last_index]
        animations.append(FadeOut(last_square))
        self.mobject.remove(last_index)
        del self.text2index[last_square["text"]]
        del self.index2square[last_index]
        if self.length() == 0:
            animations.append(self._show_empty_text())
        else:
            animations.append(self._move_to_origin())
        self.animation = AnimationGroup(*animations, lag_ratio=0.5)
        return self.animation

    def _reduce_index_by_one(self):
        new_index2square = {}
        for index in range(16):
            if index in self.index2square:
                new_index2square[index-1] = self.index2square[index]
        self.index2square = new_index2square

    def color(self, index, stroke_color=PINK1, fill_color=BACKGROUND):
        square = self.index2square[index]
        return AnimationGroup(square["box"].animate.set_stroke(stroke_color).set_fill(fill_color), square["text"].animate.set_color(stroke_color))

    def remove_first(self):
        if self.highlight_rect:
            print("You can't remove the first element during scanning. Quit scanning first.")
            return
        if self.need_update_mobject:
            self._update_table_line_mobject()
        if self.length() == 0:
            print("Array is empty")
            return
        first_index = 0
        animations = []
        first_square = self.mobject[first_index]
        animations.append(FadeOut(first_square))
        self.mobject.remove(first_index)
        del self.text2index[first_square["text"]]
        del self.index2square[first_index]
        self._reduce_index_by_one()
        self.need_update_mobject = True   # We can't update self.mobject at this time, otherwise the updated self.mobject will show up directly
        if self.length() == 0:
            animations.append(self._show_empty_text())
        else:
            animations.append(self._move_to_origin())
        self.animation = AnimationGroup(*animations, lag_ratio=0.5)
        return self.animation


class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        table = TableLine("A{{}F", show_box=False, x_position=1, y_position=2)
        self.play(table.show())
        self.play(table.initialize_scan())
        self.play(table.scan_next(2))
        self.play(table.scan_next(1))
        # self.play(table.add(4))
        # self.play(table.remove_first())
        # self.play(table.remove_last())
