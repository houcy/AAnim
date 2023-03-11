from manim import *
from manim_fonts import *
from style import *
from util import *
from company import Company


class Character():
    def __init__(self, name, image):
        self.name = name
        self.cartoon_mobject = ImageMobject(image).set_z_index(10)
        self.name_mobject = get_text(name, weight=HEAVY, font_size=24).next_to(self.cartoon_mobject, DOWN, buff=-0.1).set_z_index(10)
        self.rect_mobject = RoundedRectangle(height=2.8, width=2, corner_radius=0.2, stroke_width=3).set_fill(color=BACKGROUND, opacity=1).set_z_index(6)
        self.mobject = Group(self.cartoon_mobject, self.name_mobject, self.rect_mobject)
        # self.basic_mobject = Group(self.cartoon_mobject, self.name_mobject, self.rect_mobject)
        self.time_mobject = None
        self.scale = 1
        self.company = None
        self.is_showing = False
        self.save_state = False

    def height(self):
        return self.mobject.get_height()

    def width(self):
        return self.mobject.get_width()

    def _update_mobject(self):
        mobject_array = [self.cartoon_mobject, self.name_mobject, self.rect_mobject]
        if self.time_mobject:
            mobject_array.append(self.time_mobject)
        # if self.company:
        #     mobject_array.append(self.company.mobject)
        self.mobject = Group(*mobject_array)

    def fill_rect(self, stroke_color, fill_color):
        return AnimationGroup(self.rect_mobject.animate.set_fill(color=fill_color, opacity=1).set_stroke(color=stroke_color))

    def fade_in(self, scale=1, object=None, direction=UP, buff=2, together=False):
        self.is_showing = True
        self.scale = self.scale * scale
        if not object:
            self.mobject.scale(scale)
        else:
            self.mobject.scale(scale).next_to(object.mobject, direction, buff=buff).align_to(object.mobject, UP)
        if together:
            return FadeIn(self.cartoon_mobject, self.name_mobject, self.rect_mobject)
        else:
            return Succession(FadeIn(self.cartoon_mobject), FadeIn(self.name_mobject), Write(self.rect_mobject))

    def fade_in_by_position(self, scale=1, x_offset=0, y_offset=0, together=False):
        self.is_showing = True
        self.scale = self.scale * scale
        self.mobject.scale(scale).move_to(x_offset*RIGHT+y_offset*UP)
        if together:
            return FadeIn(self.cartoon_mobject, self.name_mobject, self.rect_mobject)
        else:
            return Succession(FadeIn(self.cartoon_mobject), FadeIn(self.name_mobject), Write(self.rect_mobject))

    def move_to(self, scale=1, x_offset=0, y_offset=0):
        self.scale = self.scale * scale
        return self.mobject.animate.scale(scale).move_to(x_offset*RIGHT + y_offset*UP)

    def shift(self, scale=1, x_offset=0, y_offset=0):
        self.scale = self.scale * scale
        return self.mobject.animate.scale(scale).shift(x_offset*RIGHT + y_offset*UP)

    def next_to(self, mobject, direction, buff=CHARACTER_CHARACTER_BUFF_VERTICAL, scale=1):
        self.scale = self.scale * scale
        return self.mobject.animate.scale(scale).next_to(mobject, direction, buff=buff)

    def align_to(self, mobject, direction, scale=1):
        self.scale = self.scale * scale
        return self.mobject.animate.scale(scale).align_to(mobject, direction)

    def move_to_top_right(self, scale=1):
        self.mobject.save_state()
        self.save_state = True
        self.scale = self.scale * scale
        return self.mobject.animate.scale(scale).to_edge(UR, buff=CHARACTER_EDGE_BUFFER)

    def back_from_top_right(self):
        if self.save_state == False:
            print("Error: state should be saved first before restoring")
            return
        self.save_state = False
        return Restore(self.mobject)

    def add_time_complexity(self, string):
        self.time_mobject = get_text(string, weight=BOLD, font_size=16*self.scale, color=GRAY).align_to(self.rect_mobject, RIGHT).align_to(self.rect_mobject, UP).shift(0.1*DOWN, 0.1*LEFT).set_z_index(10)
        self._update_mobject()
        return Write(self.time_mobject)

    def highlight(self, company_name):
        self.rect_mobject.save_state()
        self.save_state = True
        if company_name == 'MST':
            stroke_color, fill_color = MST_COMPANY
        else:
            stroke_color, fill_color = GRAY, BACKGROUND
        return self.fill_rect(stroke_color=stroke_color, fill_color=fill_color)

    def dehighlight(self):
        if self.save_state == False:
            print("Error: state should be saved first before restoring")
            return
        self.save_state = False
        return Restore(self.rect_mobject)


    # def add_company(self, name, fill_color=BACKGROUND, stroke_color=GRAY, font_size=20):
    #     animations = []
    #     self.company = Company(name, color=stroke_color, character=self, font_size=font_size, scale=self.scale)
    #     self._update_mobject()
    #     animations.append(self.fill_rect(fill_color=fill_color, stroke_color=stroke_color))
    #     animations.append(self.company.fade_in())
    #     return AnimationGroup(*animations)

    def save_state(self):
        for e in [self.cartoon_mobject, self.name_mobject, self.rect_mobject]:
            e.save_state()

    def restore(self):
        animations = []
        for e in [self.cartoon_mobject, self.name_mobject, self.rect_mobject]:
            animations.append(Restore(e))
        return AnimationGroup(*animations)
        