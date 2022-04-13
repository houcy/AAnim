from manim import *
from style import *
from queue_object import QueueObject
from stack_object import StackObject
from table_line import TableLine

LIST = [1]
E1 = "[{(}]"
E2 = "[[][]]"
E3 = "[[]]][[]"

class Show(Scene):
    def valid_parentheses(self, input_string):
        dict = {"}":"{", "]":"[", ")":"("}
        array = TableLine(input_string, show_box=False, x_position=0, y_position=2)
        self.play(array.show())
        array.initialize_scan()
        stack_object = StackObject([])
        self.play(stack_object.show())
        for paren in input_string:
            self.play(array.scan_next())
            last, color_last = stack_object.peek_last()
            if paren in dict.values():
                self.play(stack_object.append(paren))
            elif dict[paren] == last:
                self.play(color_last)
                self.play(stack_object.pop())
            else:
                self.play(color_last)
                return False
        return stack_object.array == []


    def construct(self):
        self.camera.background_color = BACKGROUND
        print(self.valid_parentheses("[{(}]"))

        # s = StackObject(LIST)
        # self.play(s.show())
        # self.play(s.append(1))
        # self.play(s.pop())
        # self.play(s.pop())

        # q = QueueObject(LIST)
        # self.play(q.show())
        # self.play(q.append(1))
        # self.play(q.pop())
        # self.play(q.append(3))
        # self.play(q.append(5))
        # self.play(q.pop())