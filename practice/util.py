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

EN_ENDING_MAP = {
    'A': {'B': None}, 
    'B': {'A': None, 'C': None}, 
    'C': {'B': None, 'D': None}, 
    'D': {'C': None, 'E': None},
    'E': {'D': None, 'F': None},
    'F': {'E': None},
    'G': {'H': None},
    'H': {'G': None, 'I': None},
    'I': {'H': None, 'J': None},
    'J': {'I': None},
    'K': {'M': None, 'L': None},
    'L': {'K': None, 'N': None},
    'M': {'K': None, 'N': None, 'O': None},
    'N': {'L': None, 'M': None, 'P': None},
    'O': {'M': None, 'P': None},
    'P': {'N': None, 'O': None},
    'Q': {'R': None, 'S': None},
    'R': {'Q': None},
    'S': {'Q': None, 'T': None},
    'T': {'S': None, 'V': None},
    'U': {'V': None},
    'V': {'T': None, 'U': None},
    'W': {'X': None, 'Y': None},
    'X': {'W': None},
    'Y': {'W': None, 'Z': None},
    'Z': {'Y': None},
    'AA': {'AB': None, 'AC': None},
    'AB': {'AA': None, 'AD': None},
    'AC': {'AA': None, 'AD': None, 'AE': None, 'AF': None},
    'AD': {'AB': None, 'AC': None},
    'AE': {'AC': None},
    'AF': {'AC': None},
    'AG': {'AH': None},
    'AH': {'AI': None, 'AG': None, 'AK': None},
    'AI': {'AH': None},
    'AJ': {'AK': None},
    'AK': {'AJ': None, 'AL': None, 'AH': None},
    'AL': {'AK': None},
    'AM': {'AN': None, 'AO': None},
    'AN': {'AM': None, 'AP': None},
    'AO': {'AM': None, 'AP': None, 'AQ': None},
    'AP': {'AN': None, 'AO': None, 'AR': None},
    'AQ': {'AO': None, 'AR': None},
    'AR': {'AP': None, 'AQ': None},
    'AS': {'AT': None, 'AU': None},
    'AT': {'AS': None},
    'AU': {'AS': None, 'AV': None, 'AW': None},
    'AV': {'AU': None},
    'AW': {'AX': None, 'AU': None},
    'AX': {'AW': None},
}
EN_ENDING_POSITION = {
    'A': (0,0), 'B': (2,0), 'C': (2,2), 'D': (0,2), 'E': (0,4), 'F': (2,4), 
    'G': (3,4), 'H': (3,0), 'I': (5,0), 'J': (5,4), 'K': (6,4), 'L': (8,4), 
    'M': (6,2), 'N': (8,2), 'O': (6,0), 'P': (8,0), 'Q': (9,4), 'R': (11,4), 
    'S': (9,2), 'T': (11,2), 'U': (9,0), 'V': (11,0), 'W': (12,4), 'X': (14,4), 
    'Y': (12,0), 'Z': (14,0), 'AA': (15,4), 'AB': (17,4), 'AC': (15,2), 'AD': (17,2), 
    'AE': (15,0), 'AF': (17,0), 'AG': (18,4), 'AH': (19,4), 'AI': (20,4), 'AJ': (18,0), 
    'AK': (19,0), 'AL': (20,0), 'AM': (21,4), 'AN': (23,4), 'AO': (21,2), 'AP': (23,2), 
    'AQ': (21,0), 'AR': (23,0), 'AS': (24,4), 'AT': (26,4), 'AU': (24,2), 'AV': (26,2), 
    'AW': (24,0), 'AX': (26,0)
}

def watermark(is_chinese=False):
    if not is_chinese:
        t1 = Text("computer", color=GRAY, weight=BOLD, font=FONT, font_size=110).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100)
        t2 = Text("psycology", color=GRAY, weight=BOLD, font=FONT, font_size=110).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100).next_to(t1, DOWN, buff=0.3)
        return VGroup(t1, t2).move_to(ORIGIN)
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

def endding(language='EN'):
    from straight_graph import StraightGraph
    from graph import GraphObject
    if language == 'CH':
        new_position_2 = scale_position(SANLIAN_POSITION_2, 2, 2)
        graph = StraightGraph(SANLIAN_MAP_2, new_position_2, edge_radius=1.5, node_radius=SMALL_RADIUS, tip_length=TIP_LENGTH_FOR_CURVED_LINE-0.05, tip_width=TIP_LENGTH_FOR_CURVED_LINE-0.05)
        animations = []
        animations.append(FadeIn(graph.mobject()))
        zan = graph.value2node['赞']
        bi = graph.value2node['币']
        cang = graph.value2node['藏']
        zan2bi = graph.get_edge(zan, bi)
        bi2cang = graph.get_edge(bi, cang)
        animations.append(zan.color(fill_color=PINK2, stroke_color=GRAY, stroke_width=WIDTH))
        animations.append(zan2bi.highlight(color=PINK2, change_tip_width=False, width=WIDTH))
        animations.append(bi.color(fill_color=GRAY, stroke_color=GRAY, stroke_width=WIDTH))
        animations.append(bi2cang.highlight(color=PINK2, change_tip_width=False, width=WIDTH))
        animations.append(cang.color(fill_color='#FDF8CA', stroke_color=GRAY, stroke_width=WIDTH))
        return Succession(*animations, lag_ratio=1)
    elif language == 'EN':
        new_position = scale_position(EN_ENDING_POSITION, 0.35, 0.4)
        graph = GraphObject(EN_ENDING_MAP, new_position, edge_radius=1.5, node_radius=0.08, font_color=BACKGROUND, font_size=0)
        animations = []
        animations.append(graph.fade_in())
        for node in graph.get_nodes():
            animations.append(node.color(stroke_color='#FF0000', fill_color='#FF0000'))
        for edge in graph.get_edges():
            animations.append(edge.highlight(color='#FF0000', width=WIDTH))
        return Succession(*animations, lag_ratio=0.1)


def get_subtitle_mobject(graph, english_string='', chinese_string='', language='EN', legend_graph_buff=0.5, subtitle_alignment=None, subtitle_position='TOP'):
    text = None
    if language == 'CH':
        text = chinese_string
    elif language == 'EN':
        text = english_string
    text_check_mobject = get_text(text, font_size=SMALL_FONT_SIZE*2, weight=ULTRAHEAVY).scale(0.5)
    # Place the subtitle on TOP/DOWN to the graph
    if subtitle_position == 'UP':
        text_check_mobject = text_check_mobject.next_to(graph.graph_mobject, UP, buff=legend_graph_buff)
    elif subtitle_position == 'DOWN':
        text_check_mobject = text_check_mobject.next_to(graph.graph_mobject, DOWN, buff=legend_graph_buff)
    # Aligh the subtitle on LEFT/RIGHT/CENTER to the graph
    if subtitle_alignment:
        text_check_mobject = text_check_mobject.align_to(graph.graph_mobject, alignment)
    return text_check_mobject