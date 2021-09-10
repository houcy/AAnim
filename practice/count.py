from manimlib import *

class Count(Animation):
    def __init__(self, number, start, end):
        super().__init__(number)
        self.start = start
        self.end = end
    
    def interpolate_mobject(self, alpha):
        value = self.start + alpha * (self.end - self.start)
        self.mobject.set_value(value)

class CountScene(Scene):
    def construct(self):
        number = DecimalNumber(number=0, num_decimal_places=0)
        number.add_updater(lambda number: number.move_to(ORIGIN))
        self.add(number)
        self.wait(2)
        self.play(Count(number, 0, 50), rate_func=linear)
        

