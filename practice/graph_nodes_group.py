from manim import *
from manim_fonts import *
from style import *


class GraphNodesGroup:
    def __init__(self, list_nodes=None):
        self.list_nodes = list_nodes
        self.circle_mobject = None
        self.key_mobject = None
        self.text_mobject = None

    def get_mobject(self):
        if self.key_mobject:
            return VGroup(self.circle_mobject, self.text_mobject, self.key_mobject)
        else:
            return VGroup(self.circle_mobject, self.text_mobject)
    
    def add(self, n):
        self.list_nodes.append(n)

    def remove(self, n):
        if n in self.list_nodes:
            self.list_nodes.remove(n)

    def get_key_mobject(self):
        mobject = VGroup()
        for n in self.list_nodes:
            if n.key_mobject:
                mobject += n.key_mobject
        return mobject

    def get_circle_mobject(self):
        mobject = VGroup()
        for n in self.list_nodes:
            if n.circle_mobject:
                mobject += n.circle_mobject
        return mobject

    def get_text_mobject(self):
        mobject = VGroup()
        for n in self.list_nodes:
            if n.circle_mobject:
                mobject += n.text_mobject
        return mobject

    def disappear(self, has_text=False):
        self.circle_mobject = self.get_circle_mobject()
        self.key_mobject = self.get_key_mobject()
        self.circle_mobject.save_state()
        self.key_mobject.save_state()
        if has_text:
            self.text_mobject = self.get_text_mobject()
            self.text_mobject.save_state()
            return AnimationGroup(self.circle_mobject.animate.set_stroke(color=BACKGROUND).set_fill(color=BACKGROUND), self.key_mobject.animate.set_color(color=BACKGROUND), self.text_mobject.animate.set_color(color=BACKGROUND))
        else:
            return AnimationGroup(self.circle_mobject.animate.set_stroke(color=BACKGROUND).set_fill(color=BACKGROUND), self.key_mobject.animate.set_color(color=BACKGROUND))


    def appear(self, has_text=False):
        if has_text:
            return AnimationGroup(Restore(self.circle_mobject), Restore(self.key_mobject), Restore(self.text_mobject))
        else:
            return AnimationGroup(Restore(self.circle_mobject), Restore(self.key_mobject))

    def color(self, key_color=PINK1, text_color=GRAY, stroke_color=PINK1, fill_color=BACKGROUND, stroke_width=WIDTH, key_width=0, has_key=False):
        circle_mobject = self.get_circle_mobject()
        if has_key:
            key_mobject = self.get_key_mobject()
            return AnimationGroup(circle_mobject.animate.set_stroke(color=stroke_color, width=stroke_width).set_fill(color=fill_color), key_mobject.animate.set_color(color=key_color).set_stroke(width=key_width))
        else:
            text_mobject = self.get_text_mobject()
            return AnimationGroup(circle_mobject.animate.set_stroke(color=stroke_color, width=stroke_width).set_fill(color=fill_color), text_mobject.animate.set_color(color=text_color).set_stroke(width=key_width))     

    def flash_keys(self, color=BACKGROUND):
        key_mobject = self.key_mobject()
        animations = [key_mobject.animate.set_color(color), key_mobject.animate.set_color(GRAY)]
        return animations