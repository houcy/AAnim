from style import *
from manim import *

class Curved_Arrow:
    def __init__(self, start, end, color=GRAY, stroke_width=WIDTH, radius=EDGE_RADIUS, tip_length=TIP_LENGTH_FOR_CURVED_LINE):
        self.mobject = ArcBetweenPoints(start, end, radius=radius, color=color, stroke_width=stroke_width)
        self.mobject.add_tip(tip_length=tip_length)