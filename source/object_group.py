from manim import *
from manim_fonts import *
from style import *
from util import *
from general_edge import GeneralEdge
from company import Company


class ObjectGroup():
    def __init__(self, object_list):
        self.object_list = object_list
        self.group = Group(*[object.mobject for object in object_list])

    def _update_character_scale(self, scale):
        for object in self.object_list:
            if hasattr(object, 'scale'):
                object.scale *= scale

    def next_to_company(self, object, scale=1, buff=COMPANY_CHARACTER_BUFF):
        self._update_character_scale(scale)
        return self.group.animate.scale(scale).next_to(object.mobject, DOWN, buff=buff).align_to(object.mobject, LEFT)