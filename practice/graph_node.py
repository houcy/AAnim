from manim import *
from manim_fonts import *
from style import *
from util import *

# z_index: edge: 0, circle: 1, text: 3, key: 5
class GraphNode:
    def __init__(self, value, position_x, position_y, is_music_note=False, node_radius=RADIUS, font_color=GRAY, font_size=VALUE_SIZE):
        self.value = value
        self.neighbor2edge = {}
        self.neighbors = []
        self.edges = []
        self.position_x = position_x
        self.position_y = position_y
        self.mobject = None
        self.text_mobject = None
        self.circle_mobject = None
        self._create_mobject(is_music_note=is_music_note, node_radius=node_radius, font_color=font_color, font_size=font_size)
        self.key = None
        self.key_mobject = None
        self.animations = None
        self.rect = None
        self.parent = None  # for Union-Find
        self.children = []  # for Union-Find
        self.is_isolated = True
        self.is_showing = False
        self.variable_name = None
        self.min_edge = None
    
    def _create_mobject(self, is_music_note, node_radius, font_color, font_size):
        """
        Convert a node to an MObject so that it shows on the canvas
        """
        self.circle_mobject = Circle(radius=node_radius).set_stroke(color=LINE_COLOR, width=WIDTH).set_fill(BACKGROUND, opacity=1.0).set_z_index(1).shift(RIGHT * self.position_x + UP * self.position_y)
        if not is_music_note:
            count_digit = len(str(self.value))
            if count_digit >= 3:
                font_size = font_size - (count_digit - 2) * 5
            self.text_mobject = Text(str(self.value), color=font_color, font=FONT, weight=BOLD, font_size=font_size).set_z_index(3).shift(self.circle_mobject.get_center())

        else:
            # for music note
            value = str(self.value)
            note, octave = value[0], value[1]
            note_mobject = Text(note, color=LINE_COLOR, font=FONT, weight=BOLD, font_size=VALUE_SIZE).set_z_index(3)
            octave_mobject = Text(octave, color=LINE_COLOR, font=FONT, weight=BOLD, font_size=TINY_VALUE_SIZE).set_z_index(3).next_to(note_mobject, RIGHT).align_to(note_mobject, DOWN).shift(0.23*LEFT + 0.05*DOWN)
            self.text_mobject = VDict({"note": note_mobject, "octave": octave_mobject})
            self.text_mobject.move_to(self.circle_mobject.get_center())
        self.mobject = VDict([("c", self.circle_mobject), ("t", self.text_mobject)])

    def mobjects(self):
        m = VDict([("c", self.circle_mobject)])
        if self.text_mobject:
            m["t"] = self.text_mobject
        if self.key_mobject:
            m["k"] = self.key_mobject
        return m

    def initialize_key(self, key, show_value=False):
        animations = []
        key_string = ''
        if key == float('inf'):
            key_string = '∞'
        elif isinstance(key, int):
            key_string = str(key)
        else:
            print("Failed to initialize key: need passing an integer")
            return
        self.key = key
        if show_value:
            new_text_mobject = None
            if show_value == 'BACK':
                new_text_mobject = get_text(str(self.value), NODE_NAME_BACKGROUND_SIZE, color=NODE_NAME_BACKGROUND_COLOR, weight=NODE_NAME_BACKGROUND_WEIGHT).move_to(self.mobject.get_center()).set_fill(opacity=NODE_NAME_BACKGROUND_OPACITY).set_z_index(3)
            if show_value == 'TOP':
                new_text_mobject = get_text(str(self.value), SMALL_FONT_SIZE, color=GRAY, weight=BOLD).next_to(self.mobject, UP, buff=0.15)
            animations.append(ReplacementTransform(self.text_mobject, new_text_mobject))
            self.text_mobject = new_text_mobject
            self.key_mobject = get_text(key_string, font_size=KEY_SIZE, weight=BOLD).move_to(self.circle_mobject.get_center()).set_z_index(5)
            animations.append(FadeIn(self.key_mobject))
        else:
            self.text_mobject.save_state()
            self.key_mobject = get_text(key_string, font_size=KEY_SIZE, weight=BOLD).move_to(self.circle_mobject.get_center()).set_z_index(5)
            animations.append(ReplacementTransform(self.text_mobject, self.key_mobject))
            self.text_mobject = None
        self.animations = animations    # If show_value is True, there will be 2 animations: Transform and FadeIn; Otherwise, only 1 animation
        return AnimationGroup(*animations, lag_ratio=1)
    
    def update_key(self, key, color=GRAY):
        animations = []
        new_key_mobject = get_text(str(key), font_size=KEY_SIZE, weight=BOLD, color=color).move_to(self.circle_mobject.get_center()).set_z_index(5)
        animations.append(ReplacementTransform(self.key_mobject, new_key_mobject))
        self.key = key
        self.key_mobject = new_key_mobject
        self.animations = animations
        return AnimationGroup(*animations)

    def highlight_stroke(self, color=HIGHLIGHT_STROKE):
        """
        Change the stroke color of the node to be highlight color
        """
        return AnimationGroup(self.circle_mobject.animate.set_stroke(color=color), Wait())

    def highlight_stroke_and_change_shape(self, fill_color=PINK3, stroke_color=PINK1, shape="ROUNDEDRECTANGLE"):
        """
        Change the stroke color of the node to be highlight color
        """
        circle = self.circle_mobject
        circle.save_state()
        if shape == "ROUNDEDRECTANGLE":
            self.rect = RoundedRectangle(corner_radius=0.2, height=HIGHLIGHT_RECTANGLE_WIDTH, width=HIGHLIGHT_RECTANGLE_WIDTH).set_fill(fill_color, 1).set_stroke(color=stroke_color, width=WIDTH+1).move_to(circle.get_center()).set_z_index(1)
        elif shape == "HEART":
            self.rect = SVGMobject("heart.svg", height=0.7, fill_color=PINK3).move_to(circle.get_center()).set_z_index(1)
        return AnimationGroup(ReplacementTransform(circle, self.rect), Wait())

    def dehighlight_stroke_and_change_shape(self):
        """
        Change the stroke color of the node to be highlight color
        """
        return AnimationGroup(Wait(), FadeOut(self.rect), Restore(self.circle_mobject), Wait())

    def mark_pink1(self):
        """
        Fill this node as PINK1 (dark pink)
        """
        return AnimationGroup(self.circle_mobject.animate.set_fill(PINK1).set_stroke(PINK2), self.text_mobject.animate.set_color(BACKGROUND))

    def color(self, fill_color=PINK2, stroke_color=PINK3, stroke_width=WIDTH, text_color=BACKGROUND, has_key=False):
        """
        Fill this node as PINK (light pink)
        """
        if not has_key:
            return AnimationGroup(self.circle_mobject.animate.set_fill(fill_color).set_stroke(stroke_color, width=stroke_width), self.text_mobject.animate.set_color(text_color))
        elif self.text_mobject:
            return AnimationGroup(self.circle_mobject.animate.set_fill(fill_color).set_stroke(stroke_color, width=stroke_width), self.key_mobject.animate.set_color(text_color), self.text_mobject.animate.set_color(text_color))
        else:
            return AnimationGroup(self.circle_mobject.animate.set_fill(fill_color).set_stroke(stroke_color, width=stroke_width), self.key_mobject.animate.set_color(text_color))

    def mark_pink3(self):
        """
        Fill this node as PINK (light pink)
        """
        return AnimationGroup(self.circle_mobject.animate.set_fill(PINK3).set_stroke(PINK3), self.text_mobject.animate.set_color(BACKGROUND))
    
    def mark_blue1(self):
        """
        Fill this node as BLUE
        """
        return AnimationGroup(self.circle_mobject.animate.set_fill(BLUE1).set_stroke(BLUE1), self.text_mobject.animate.set_color(BACKGROUND))
    
    def mark_line_pink1(self, neighbor):
        """
        Fill a line pointing to 'neighbor' as PINK
        """
        return self.neighbor2edge[neighbor].mobject.animate.set_fill(PINK1).set_stroke(PINK1)

    def mark_line_blue1(self, neighbor):
        """
        Fill a line pointing to 'neighbor' as BLUE
        """
        return self.neighbor2edge[neighbor].mobject.animate.set_fill(BLUE1).set_stroke(BLUE1)

    def highlight(self, stroke_color=PINK5, stroke_width=WIDTH):
        self.circle_mobject.save_state()
        self.save_state = True
        return AnimationGroup(self.circle_mobject.animate.set_stroke(color=stroke_color, width=stroke_width))

    def dehighlight(self):
        if self.save_state:
            self.save_state = False
            return AnimationGroup(Restore(self.circle_mobject))
            
    def fade_out(self):
        self.is_showing = False
        return FadeOut(self.mobjects())

    def fade_in(self):
        self.is_showing = True
        return FadeIn(self.mobject())

    def fade_in_variable(self, variable_name, show_background=True, direction='UP'):
        text = Text(variable_name, color=GRAY, font=FONT, weight=NORMAL, font_size=WEIGHT_SIZE).set_z_index(10).set_stroke(color=EDGE_STROKE_COLOR, width=EDGE_STROKE_WIDTH)
        if direction == 'UP':
            text.move_to(self.circle_mobject.get_top()).shift(UP * 0.22)
        elif direction == 'LEFT':
            text.move_to(self.circle_mobject.get_left()).shift(LEFT * 0.22)
        elif direction == 'RIGHT':
            text.move_to(self.circle_mobject.get_right()).shift(RIGHT * 0.22)
        elif direction == 'DOWN':
            text.move_to(self.circle_mobject.get_bottom()).shift(DOWN * 0.22)
        side_length = VARIABLE_SQUARE_SIZE
        text_background = RoundedRectangle(corner_radius=0.05, width=side_length, height=side_length).set_stroke(color=GRAY, width=2).set_fill(BACKGROUND, opacity=1.0).set_z_index(9).move_to(text.get_center())
        self.variable_name = variable_name
        if show_background:
            self.variable_mobject = VDict([("text", text), ("text_background", text_background)])
        else:
            self.variable_mobject = VDict([("text", text)])
        return FadeIn(self.variable_mobject)

    def fade_out_variable(self):
        return FadeOut(self.variable_mobject)

class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        node = GraphNode(value='A', position_x=1, position_y=1)
        self.add(node.mobject)
        self.play(node.color(fill_color=PINK3, stroke_color=PINK1, stroke_width=WIDTH+2))
        self.play(node.color(fill_color=PINK2, stroke_color=PINK2, stroke_width=WIDTH))
        # self.play(node.highlight_stroke_and_change_shape(shape = "HEART"))