from manim import *
from style import *

class Table():
    def __init__(self, array, is_mobject=False, buff=0.5):
        """
        Parameter
        1. array: a list of content(int or str)
        2. buff: the distance between the first line and the second line
        """
        self.animation = []
        self.first_line = None # A VDict object that is up to 15 elements
        self.second_line = None
        self.length = len(array)
        self.buff = buff
        self.table = []
        self.is_mobject = is_mobject
        if self.length >= 32:
            print("Array is too long")
            return
        if is_mobject:
            for mob in array:
                square = VDict([("box", Square(side_length=TABLE_SIDE_LENGTH)), ("text", mob)])
                self.table.append(square)
        else:
            for value in array:
                mobject = self._create_text_mobject(value)
                square = VDict([("box", Square(side_length=TABLE_SIDE_LENGTH)), ("text", mobject)])
                self.table.append(square)
        if self.length <= 15:
            self.first_line = VDict(zip(list(range(self.length)), self.table)).arrange(buff=0)
            self.animation = [FadeIn(x) for x in self.table]
        else:
            self.first_line = VDict(zip(list(range(15)), self.table[:15])).arrange(buff=0)
            self.second_line = VDict(zip(list(range(15, self.length)), self.table[15:])).arrange(buff=0)
            self.second_line.next_to(self.first_line, direction = DOWN, buff=self.buff) 
            self.animation = [FadeIn(x) for x in self.table]

    def add(self, value):
        if self.length >= 32:
            print("Array is too long")
            return
        animation = []
        mobject = None
        if self.is_mobject:
            mobject = value
        else:
            mobject = self._create_text_mobject(value)
        square = VGroup(Square(side_length=TABLE_SIDE_LENGTH), mobject)
        if self.length < 15:
            square.next_to(self.first_line, RIGHT, buff=0)
            self.first_line = self.first_line.add([(self.length, square)])
            animation.append(FadeIn(square))
            position_y = self.first_line.get_y()
            animation.append(self.first_line.animate.move_to([0, position_y, 0]))
        elif self.length == 15:
            self.second_line = self.second_line.add([(self.length, square)])
            self.second_line.next_to(self.first_line, direction = DOWN, buff=self.buff) 
            square.next_to(self.second_line, RIGHT, buff=0)
            animation.append(FadeIn(square))
            position_y = self.second_line.get_y()
            animation.append(self.second_line.animate.move_to([0, position_y, 0]))    
        else:
            square.next_to(self.second_line, RIGHT, buff=0)
            self.second_line = self.second_line.add([(self.length, square)])
            animation.append(FadeIn(square))
            position_y = self.second_line.get_y()
            animation.append(self.second_line.animate.move_to([0, position_y, 0]))        
        self.animation = AnimationGroup(*animation)
        self.length += 1
        return self.animation

    def swap(self, index, index_to_swap):
        mobject, mobject_to_swap = None, None
        if self.is_mobject:
            mobject, mobject_to_swap = index, index_to_swap
        else:
            if index < 15:
                mobject = self.first_line[index]["text"]
            else:
                mobject = self.second_line[index]["text"]
            if index_to_swap < 15:
                mobject_to_swap = self.first_line[index_to_swap]["text"]
            else:
                mobject_to_swap = self.second_line[index_to_swap]["text"]
        return Swap(mobject, mobject_to_swap)

    def remove(self):
        if self.length == 0:
            print("Array is empty")
            return
        animation = []
        if self.length <=15:
            animation.append(FadeOut(self.first_line[self.length-1]))
            self.first_line.remove(self.length-1)
            position_y = self.first_line.get_y()
            animation.append(self.first_line.animate.move_to([0, position_y, 0]))
        else:
            animation.append(FadeOut(self.second_line[self.length-1]))
            self.second_line.remove(self.length-1)
            if self.length > 16:
                position_y = self.second_line.get_y()
                animation.append(self.second_line.animate.move_to([0, position_y, 0]))
        self.animation = AnimationGroup(*animation, lag_ratio=0.5)
        self.length -= 1
        return self.animation
        
    def _create_text_mobject(self, value):
        return Tex(str(value), color=LINE_COLOR).scale(FONT_SIZE)


# class Example(Scene):
#     def construct(self):
#         self.camera.background_color = BACKGROUND_COLOR
#         table = Table([i for i in range(18)])
#         self.play(*table.animation)
#         self.play(table.remove())
#         self.play(table.add(22))
#         self.play(table.swap(2, 15))

#         mobject1 = Tex(str(0), color=LINE_COLOR).scale(FONT_SIZE)
#         mobject2 = Tex(str(1), color=LINE_COLOR).scale(FONT_SIZE)
#         mobject3 = Tex(str(3), color=LINE_COLOR).scale(FONT_SIZE)
#         table = Table([mobject1, mobject2, mobject3], is_mobject=True)
#         self.play(*table.animation)
#         self.play(table.swap(mobject1, mobject3))
        
