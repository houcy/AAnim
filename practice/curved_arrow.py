from style import *
from manim import *

class Curved_Arrow:
    def __init__(self, start, end, color=GRAY, stroke_width=WIDTH, tip_length=TIP_LENGTH_FOR_CURVED_LINE, edge_radius=EDGE_RADIUS):
        self.mobject = ArcBetweenPoints(start, end, radius=edge_radius, color=color, stroke_width=stroke_width)
        self.mobject.add_tip(tip_length=tip_length)