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

ALL_ALPHA_POSITION = {
    '0': (0, 2), '1': (1, 2), '2': (2, 2), '3': (3, 2), '4': (4, 2),
    '5': (5, 2),'6': (6, 2),'7': (7, 2),'8': (8, 2),'9': (9, 2),'10': (10, 2),
    '11': (11, 2),'12': (12, 2),'13': (13, 2),'14': (14, 2),'15': (15, 2),
    '16': (16, 2),'17': (17, 2),'18': (18, 2),'19': (19, 2),
    '30': (0, 1),'31': (1, 1),'32': (2, 1),'33': (3, 1),'34': (4, 1),
    '35': (5, 1),'36': (6, 1),'37': (7, 1),'38': (8, 1),'39': (9, 1),
    '40': (10, 1),'41': (11, 1),'42': (12, 1),'43': (13, 1),'44': (14, 1),
    '45': (15, 1),'46': (16, 1),'47': (17, 1),'48': (18, 1),'49': (19, 1),
    '60': (0, 0),'61': (1, 0),'62': (2, 0),'63': (3, 0),'64': (4, 0),
    '65': (5, 0),'66': (6, 0),'67': (7, 0),'68': (8, 0),'69': (9, 0),
    '70': (10, 0),'71': (11, 0),'72': (12, 0),'73': (13, 0),'74': (14, 0),
    '75': (15, 0),'76': (16, 0),'77': (17, 0),'78': (18, 0),'79': (19, 0)
}

ALL_ALPHA_MAP = {
    '0': {'1': None, '30': None, '31': None},
    '1': {'0': None, '2': None, '31': None},
    '2': {'1': None, '3': None, '31': None, '32': None, '33': None},
    '3': {'2': None, '4': None, '33': None},
    '4': {'3': None, '5': None, '33': None, '34': None, '35': None},
    '5': {'4': None, '6': None, '35': None},
    '6': {'5': None, '7': None, '35': None, '36': None, '37': None},
    '7': {'6': None, '8': None, '37': None},
    '8': {'7': None, '9': None, '37': None, '38': None, '39': None},
    '9': {'8': None, '10': None, '39': None},
    '10': {'9': None, '11': None, '39': None, '40': None, '41': None},
    '11': {'10': None, '12': None, '41': None},
    '12': {'11': None, '13': None, '41': None, '42': None, '43': None},
    '13': {'12': None, '14': None, '43': None},
    '14': {'13': None, '15': None, '43': None, '44': None, '45': None},
    '15': {'14': None, '16': None, '45': None},
    '16': {'15': None, '17': None, '45': None, '46': None, '47': None},
    '17': {'16': None, '18': None, '47': None},
    '18': {'17': None, '19': None, '47': None, '48': None, '49': None},
    '19': {'18': None, '49': None},
    '30': {'0': None, '31': None, '60': None},
    '31': {'0': None, '1': None, '2': None, '30': None, '32': None, '60': None, '61': None, '62': None},
    '32': {'2': None, '31': None, '33': None, '62': None},
    '33': {'2': None, '3': None, '4': None, '32': None, '34': None, '62': None, '63': None, '64': None},
    '34': {'4': None, '33': None, '35': None, '64': None},
    '35': {'4': None, '5': None, '6': None, '34': None, '36': None, '64': None, '65': None, '66': None},
    '36': {'6': None, '35': None, '37': None, '66': None},
    '37': {'6': None, '7': None, '8': None, '36': None, '38': None, '66': None, '67': None, '68': None},
    '38': {'8': None, '37': None, '39': None, '68': None},
    '39': {'8': None, '9': None, '10': None, '38': None, '40': None, '68': None, '69': None, '70': None},
    '40': {'10': None, '39': None, '41': None, '70': None},
    '41': {'10': None, '11': None, '12': None, '40': None, '42': None, '70': None, '71': None, '72': None},
    '42': {'12': None, '41': None, '43': None, '72': None},
    '43': {'12': None, '13': None, '14': None, '42': None, '44': None, '72': None, '73': None, '74': None},
    '44': {'14': None, '43': None, '45': None, '74': None},
    '45': {'14': None, '15': None, '16': None, '44': None, '46': None, '74': None, '75': None, '76': None},
    '46': {'16': None, '45': None, '47': None, '76': None},
    '47': {'16': None, '17': None, '18': None, '46': None, '48': None, '76': None, '77': None, '78': None},
    '48': {'18': None, '47': None, '49': None, '78': None},
    '49': {'18': None, '19': None, '48': None, '78': None, '79': None},
    '60': {'30': None, '31': None, '61': None},
    '61': {'31': None, '60': None, '62': None},
    '62': {'31': None, '32': None, '33': None, '61': None, '63': None},
    '63': {'33': None, '62': None, '64': None},
    '64': {'33': None, '34': None, '35': None, '63': None, '65': None},
    '65': {'35': None, '64': None, '66': None},
    '66': {'35': None, '36': None, '37': None, '65': None, '67': None},
    '67': {'37': None, '66': None, '68': None},
    '68': {'37': None, '38': None, '39': None, '67': None, '69': None},
    '69': {'39': None, '68': None, '70': None},
    '70': {'39': None, '40': None, '41': None, '69': None, '71': None},
    '71': {'41': None, '70': None, '72': None},
    '72': {'41': None, '42': None, '43': None, '71': None, '73': None},
    '73': {'43': None, '72': None, '74': None},
    '74': {'43': None, '44': None, '45': None, '73': None, '75': None},
    '75': {'45': None, '74': None, '76': None},
    '76': {'45': None, '46': None, '47': None, '75': None, '77': None},
    '77': {'47': None, '76': None, '78': None},
    '78': {'47': None, '48': None, '49': None, '77': None, '79': None},
    '79': {'49': None, '78': None},
}

like_map = [
    ('6', '36'), ('36', '66'), ('66', '67'), ('8', '38'), ('38', '68'), 
    ('9', '39'), ('39', '69'), ('10', '39'), ('39', '70'), ('11', '12'), 
    ('11', '41'), ('41', '42'), ('41', '71'), ('71', '72')
]
comment_map = [
    ('0', '30'), ('30', '60'), ('0', '1'), ('60', '61'),
    ('2', '3'), ('2', '32'), ('32', '62'), ('62', '63'), ('63', '33'), ('3', '33'),
    ('4', '34'), ('34', '64'), ('4', '35'), ('35', '6'), ('6', '36'), ('36', '66'),
    ('8', '38'), ('38', '68'), ('8', '39'), ('39', '10'), ('10', '40'), ('40', '70'),
    ('11', '12'), ('11', '41'), ('41', '71'), ('71', '72'), ('41', '42'), 
    ('14', '44'), ('44', '74'), ('14', '45'), ('45', '76'), ('76', '46'), ('46', '16'), 
    ('17', '18'), ('18', '19'), ('18', '48'), ('48', '78'),
]

subscribe_map = [
    ('0', '1'), ('0', '30'), ('30', '31'), ('31', '61'), ('61', '60'),
    ('2', '32'), ('32', '62'), ('62', '63'), ('63', '33'), ('33', '3'),
    ('4', '5'), ('4', '34'), ('34', '35'), ('64', '65'), ('34', '64'), ('35', '65'), ('5', '35'), 
    ('6', '7'), ('6', '36'), ('36', '37'), ('37', '67'), ('67', '66'), 
    ('8', '9'), ('8', '38'), ('38', '68'), ('68', '69'),
    ('11', '12'), ('12', '42'), ('11', '41'), ('42', '41'), ('41', '71'), ('41', '72'),
    ('13', '43'), ('43', '73'), 
    ('14', '15'), ('44', '45'), ('74', '75'), ('14', '44'), ('44', '74'), ('15', '45'), ('45', '75'),
    ('16', '17'), ('46', '47'), ('76', '77'), ('16', '46'), ('46', '76'),
]

def watermark(is_chinese=False):
    if not is_chinese:
        t1 = Text("computer", color=GRAY, weight=BOLD, font=FONT, font_size=110).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100)
        t2 = Text("psychology", color=GRAY, weight=BOLD, font=FONT, font_size=110).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100).next_to(t1, DOWN, buff=0.3)
        return VGroup(t1, t2).move_to(ORIGIN)
    else:
        t1 = Text("计算之心", color=GRAY, weight=ULTRAHEAVY, font=FONT, font_size=130).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100)
        t2 = Text("b i l i b i l i", color=GRAY, weight=ULTRAHEAVY, font=FONT, font_size=90, width=6.5).set_fill(opacity=WATERMARK_OPACITY).set_z_index(100).next_to(t1, DOWN, buff=0.3)
        # heart = SVGMobject("heart.svg", height=0.8).set_fill(color=PINK3, opacity=WATERMARK_OPACITY).set_z_index(100).next_to(t1, DOWN, buff=0.3).align_to(t1, LEFT).shift(0.2*RIGHT+0.02*DOWN)
        return VGroup(t1, t2).move_to(ORIGIN)

def show_title(text, up_mobject=None, title_scale=0.25, font_size=TITLE_SIZE):
    t = None
    animations = []
    if not up_mobject:
        # The Title
        t = Paragraph(*text, color=GRAY, font=FONT, weight="BOLD", font_size=font_size)
        animations = [Write(t), t.animate.scale(title_scale).set_color(GRAY_OUT).to_edge(UL, buff=0.7).shift(0.1 * UP)]
    else:
        # The secondary title
        t = Text(text, color=GRAY, font=FONT, weight="BOLD", font_size=SECONDARY_TITLE_SIZE)
        animations = [Write(t), t.animate.scale(0.5).next_to(up_mobject, DOWN, buff=0.2).align_to(up_mobject, LEFT)]
    return t, Succession(*animations)


def get_text(text, font_size=VALUE_SIZE, color=GRAY, weight=NORMAL, width=None, line_spacing=-1):
    if font_size < 40:
        return Text(text, color=color, font=FONT, weight=weight, font_size=font_size*2, line_spacing=line_spacing).scale(0.5)
    else:
        return Text(text, color=color, font=FONT, weight=weight, font_size=font_size, line_spacing=line_spacing)

def show_title_for_demo(text):
    title_mobject = get_text(text, font_size=TITLE_SIZE_FOR_DEMO*2, color=GRAY_OUT, weight=BOLD).scale(0.5).to_edge(UL, buff=0.7).shift(0.1 * UP)
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

def fairytale_header(language='EN'):
    if language == 'EN':
        animations = []
        title_mobject = show_title_for_demo("The Fairy Tale of Algorithms")
        text1 = 'The'
        text2 = 'Fairy Tale'
        text3 = 'of Algorithms'
        # The Title
        t1 = Text(text1, color=GRAY, font=FONT, weight="BOLD", font_size=70)
        t2 = Text(text2, color=PINK1, font=FONT, weight="BOLD", font_size=70).next_to(t1, RIGHT, buff=0.5).align_to(t1, UP)
        t3 = Text(text3, color=GRAY, font=FONT, weight="BOLD", font_size=70).next_to(t2, DOWN, buff=0.5).align_to(t1, LEFT)
        t_group1 = VGroup(t1, t2, t3)
        t_group1.move_to(ORIGIN)
        animations.append(Write(t_group1))
        animations.append(Wait(2))
        animations.append(AnimationGroup(Unwrite(t_group1), FadeIn(title_mobject)))
        return Succession(*animations)
    elif language == 'CH':
        animations = []
        title_mobject = show_title_for_demo("算法童话")
        text1 = '算法'
        text2 = '童话'
        # The Title
        t1 = Text(text1, color=GRAY, font=FONT, weight="BOLD", font_size=70)
        t2 = Text(text2, color=PINK1, font=FONT, weight="BOLD", font_size=70).next_to(t1, RIGHT, buff=0.2)
        t_group = VGroup(t1, t2).move_to(ORIGIN)
        animations.append(Write(t_group))
        animations.append(Wait(5))
        animations.append(AnimationGroup(Unwrite(t_group), FadeIn(title_mobject)))
        animations.append(Wait())
        return Succession(*animations)


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
        FONT_COLOR = PINK1
        new_position = scale_position(ALL_ALPHA_POSITION, 0.6, 0.6)
        graph = GraphObject(ALL_ALPHA_MAP, new_position, edge_radius=1.5, edge_color='#1E2947', node_radius=0.02, node_font_size=0, node_fill_color=GRAY, node_stroke_color=GRAY)
        animations = []
        animations.append(graph.fade_in(y_offset=1))
        like = graph.create_sub_graph('like', like_map)
        animations.append(like.highlight(together=False, node_fill_color=FONT_COLOR, node_stroke_color=FONT_COLOR, edge_color=FONT_COLOR, edge_width=WIDTH+4, lag_ratio=0.06))
        animations.append(Wait(2))
        animations.append(like.highlight(together=True, node_fill_color=GRAY, node_stroke_color=GRAY, edge_color='#1E2947', edge_width=WIDTH))

        comment = graph.create_sub_graph('comment', comment_map)
        animations.append(comment.highlight(together=False, node_fill_color=FONT_COLOR, node_stroke_color=FONT_COLOR, edge_color=FONT_COLOR, edge_width=WIDTH+4, lag_ratio=0.06))
        animations.append(Wait(2))
        animations.append(comment.highlight(together=True, node_fill_color=GRAY, node_stroke_color=GRAY, edge_color='#1E2947', edge_width=WIDTH))

        subscribe = graph.create_sub_graph('subscribe', subscribe_map)
        animations.append(subscribe.highlight(together=False, node_fill_color=FONT_COLOR, node_stroke_color=FONT_COLOR, edge_color=FONT_COLOR, edge_width=WIDTH+4, lag_ratio=0.06))
        animations.append(Wait(8))
        return Succession(*animations, lag_ratio=1)

        # new_position = scale_position(EN_ENDING_POSITION, 0.3, 0.3)
        # graph = GraphObject(EN_ENDING_MAP, new_position, edge_radius=1.5, node_radius=0.08, font_color=BACKGROUND, node_font_size=0)
        # animations = []
        # animations.append(graph.fade_in(y_offset=1))
        # for node in graph.get_nodes():
        #     animations.append(node.color(stroke_color=RED, fill_color=RED))
        # for edge in graph.get_edges():
        #     animations.append(edge.highlight(color=RED, width=WIDTH))
        # return Succession(*animations, lag_ratio=0.1)


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