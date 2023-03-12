from tkinter import font
from manim import *
from style import *
from code_constant import *
from graph import GraphObject
from code_block import CodeBlock
from legend import Legend
from graph_edges_group import GraphEdgesGroup
from graph_nodes_group import GraphNodesGroup
from util import *
from union_find import UnionFind
from color_generator import ColorGenerator
import copy
import manimpango

class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        title_mobject = show_title_for_demo("算法童话")
        self.add(title_mobject)
        # c = ColorGenerator()
        # colors = c.vivid_colors(7)
        # i = -3
        # for co in colors:
        #     circle = Circle(radius=RADIUS).set_fill(co, opacity=1.0).set_stroke(co).set_z_index(0)
        #     self.play(FadeIn(circle.shift(i*RIGHT)))
        #     i+=1

        k_title = Text("Kruskal", color=GRAY, font=FONT, weight=SEMIBOLD, font_size=SMALL_FONT_SIZE*2).scale(0.5).move_to(3*LEFT+2.5*UP)
        p_title = Text("Prim", color=GRAY, font=FONT, weight=SEMIBOLD, font_size=SMALL_FONT_SIZE*2).scale(0.5).move_to(-3*LEFT+2.5*UP)

        # circle = Circle(radius=RADIUS).set_fill(RED, opacity=1.0).set_stroke(RED).set_z_index(0)
        # highlight_rect = RoundedRectangle(corner_radius=0.05, width=CODE_BLOCK_WIDTH_PADDING, height=1).set_stroke(color=GRAY, width=BOX_STROKE_WIDTH)
        # line_mobject = Line([0, 0, 0], [0, 3, 0], buff=0.4, stroke_width=WIDTH).add_tip(tip_length=0.2, tip_width=0.2).set_stroke(color=GRAY, width=WIDTH).set_z_index(0)

        # png = ImageMobject("kruskal.png")
        # self.play(FadeIn(text, circle))



        self.add(k_title, p_title)

        self.play(k_title.animate.next_to(p_title, UP))


    