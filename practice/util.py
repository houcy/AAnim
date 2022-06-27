from typing import Text
from manim import *
from style import *
from manim_fonts import * 
from manim import *
from style import *
from code_constant import *




# SANLIAN_MAP_1 = {'赞': {'币': None, '藏': None}}
# SANLIAN_POSITION_1 = {'币': (0, 0), '赞': (1, 0), '藏': (2, 0)}

SANLIAN_MAP_2 = {'赞': {'币': None}, '币': {'藏': None}}
SANLIAN_POSITION_2 = {'赞': (0, 0), '币': (1, 0), '藏': (2, 0)}

EN_ENDING_MAP = {'like': {'comment': None}, 'comment': {'sub': None}}
EN_ENDING_POSITION = {'like': (0, 0), 'com"t': (1, 0), 'sub': (2, 0)}

def watermark(is_chinese=False):
    if not is_chinese:
        return Text("Compsyc", color=GRAY, weight=BOLD, font=FONT, font_size=160).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100)
    else:
        t1 = Text("计算之心", color=GRAY, weight=ULTRAHEAVY, font=FONT, font_size=130).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100)
        t2 = Text("b i l i b i l i", color=GRAY, weight=ULTRAHEAVY, font=FONT, font_size=90, width=6.5).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100).next_to(t1, DOWN, buff=0.3)
        # heart = SVGMobject("heart.svg", height=0.8).set_fill(color=PINK3, opacity=WATERMARK_OPACITY).set_z_index(100).next_to(t1, DOWN, buff=0.3).align_to(t1, LEFT).shift(0.2*RIGHT+0.02*DOWN)
        return VGroup(t1, t2).move_to(ORIGIN)

def show_title(text, up_mobject=None, title_scale=0.25):
    t, animation1, animation2 = None, None, None
    if not up_mobject:
        # The Title
        t = Paragraph(*text, color=GRAY, font=FONT, weight="BOLD", font_size=TITLE_SIZE)
        animation1 = Write(t)
        animation2 = t.animate.scale(title_scale).set_color(GRAY_OUT).to_edge(UL, buff=0.8).shift(0.2 * UP)
    else:
        # The secondary title
        t = Text(text, color=GRAY, font=FONT, weight="BOLD", font_size=SECONDARY_TITLE_SIZE)
        animation1 = Write(t)
        animation2 = t.animate.scale(0.5).next_to(up_mobject, DOWN, buff=0.2).align_to(up_mobject, LEFT)
    return t, animation1, animation2

def get_text(text, font_size=VALUE_SIZE, color=GRAY, weight=NORMAL, width=None):
    return Text(text, color=color, font=FONT, weight=weight, font_size=font_size)

def show_title_for_demo(text):
    title_mobject = get_text(text, font_size=TITLE_SIZE_FOR_DEMO*2, color=GRAY_OUT, weight=BOLD).scale(0.5).to_edge(UL, buff=0.8).shift(0.2 * UP)
    return title_mobject

def scale_position(positions, x_scale=1, y_scale=1):
    pos = {}
    for node, position in positions.items():
        x, y = position
        pos[node] = (x*x_scale, y*y_scale)
    return pos

def extract_min_node(list):
    min_so_far = float('inf')
    min_node = None
    for n in list:
        if n.key < min_so_far:
            min_so_far = n.key
            min_node = n
    list.remove(min_node)
    return min_node

def endding(is_chinese=True):
    from straight_graph import StraightGraph
    if is_chinese:
        new_position_2 = scale_position(SANLIAN_POSITION_2, 2, 2)
        graph = StraightGraph(SANLIAN_MAP_2, new_position_2, edge_radius=1.5, node_radius=SMALL_RADIUS)
        animations = []
        animations.append(FadeIn(graph.mobject()))
        zan = graph.value2node['赞']
        bi = graph.value2node['币']
        cang = graph.value2node['藏']
        zan2bi = graph.get_edge(zan, bi)
        bi2cang = graph.get_edge(bi, cang)
        animations.append(zan.color(fill_color=PINK2, stroke_color=GRAY, stroke_width=WIDTH))
        animations.append(zan2bi.highlight(color=PINK2, change_tip_width=False))
        animations.append(bi.color(fill_color=GRAY, stroke_color=GRAY, stroke_width=WIDTH))
        animations.append(bi2cang.highlight(color=PINK2, change_tip_width=False))
        animations.append(cang.color(fill_color='#FDF8CA', stroke_color=GRAY, stroke_width=WIDTH))
        return Succession(*animations, lag_ratio=1)
    else:
        new_position = scale_position(EN_ENDING_POSITION, 2, 2)
        graph = StraightGraph(EN_ENDING_MAP, new_position, edge_radius=1.5, node_radius=RADIUS)
        animations = []
        animations.append(FadeIn(graph.mobject()))
        like = graph.value2node['like']
        comment = graph.value2node['comment']
        subscribe = graph.value2node['sub']
        like2comment = graph.get_edge(like, comment)
        comment2subscribe = graph.get_edge(comment, subscribe)
        animations.append(like.color(fill_color=PINK2, stroke_color=GRAY, stroke_width=WIDTH))
        animations.append(like2comment.highlight(color=PINK2, change_tip_width=False))
        animations.append(comment.color(fill_color=GRAY, stroke_color=GRAY, stroke_width=WIDTH))
        animations.append(comment2subscribe.highlight(color=PINK2, change_tip_width=False))
        animations.append(subscribe.color(fill_color='#FDF8CA', stroke_color=GRAY, stroke_width=WIDTH))
        return Succession(*animations, lag_ratio=1)


