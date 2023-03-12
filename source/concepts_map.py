from manim import *
from manim_fonts import *
from style import *
from util import *
from general_edge import GeneralEdge
from company import Company


class ConceptsMap():
    def __init__(self, object_array):
        self.current_scale = 1
        self.mobject = None
        self.name2object = {}
        mobject_list = []
        for object in object_array:
            self.name2object[object.name] = object
            mobject_list.append(object.mobject)
        self.mobject = Group(*mobject_list)


    def _update_mobject(self):
        """
        Update the dictionary + Grow the Group()
        """
        mobject_list = []
        for object in list(self.name2object.values()):
            mobject_list.append(object.mobject)
        self.mobject = Group(*mobject_list)

    def _update_character_scale(self, scale):
        for object in list(self.name2object.values()):
            if hasattr(object, 'scale'):
                object.scale *= scale

    def add(self, object):
        if object.name in self.name2object:
            return
        self.name2object[object.name] = object
        self._update_mobject()

    def add_company(self, name, character, fill_color=BACKGROUND, stroke_color=GRAY, font_size=20):
        animations = []
        company = Company(name, color=stroke_color, character=character, font_size=font_size, scale=character.scale)
        character.company = company
        self.name2object[company.name] = company
        self._update_mobject()
        animations.append(character.fill_rect(fill_color=fill_color, stroke_color=stroke_color))
        animations.append(company.fade_in())
        return AnimationGroup(*animations)

    def show_only(self, object_to_keep):
        animations = []
        for object in list(self.name2object.values()):
            if object not in object_to_keep:
                object.is_showing = False
                animations.append(FadeOut(object.mobject))
            else:
                object.is_showing = True
        return AnimationGroup(*animations)

    def show_all(self):
        animations = []
        for object in list(self.name2object.values()):
            if not object.is_showing:
                animations.append(FadeIn(object.mobject))
        return AnimationGroup(*animations)

    def scale_all(self, scale=1):
        self._update_mobject()
        self._update_character_scale(scale)
        return self.mobject.animate.scale(scale)

    def shift(self, scale=1, x_offset=0, y_offset=0):
        self.current_scale = self.current_scale * scale
        self._update_character_scale(scale)
        self._update_mobject()
        return self.mobject.animate.scale(scale).shift(x_offset*RIGHT + y_offset*UP)

    def center(self, scale=1):
        self.current_scale = self.current_scale * scale
        self._update_character_scale(scale)
        self._update_mobject()
        return self.mobject.animate.scale(scale).move_to(ORIGIN)

    def add_edge(self, start, end, buff=0, width=WIDTH, weight=''):
        line = GeneralEdge(start, end, weight=weight, buff=buff, width=width, font_size=20*self.current_scale)        
        self.add(line)
        return line.fade_in_sequence()

    def fade_out(self):
        for object in list(self.name2object.values()):
            object.is_showing = False
        return FadeOut(self.mobject)

    def fade_in(self):
        for object in list(self.name2object.values()):
            object.is_showing = True
        return FadeIn(self.mobject)