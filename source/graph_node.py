from manim import *
from manim_fonts import *
from style import *
from util import *

# z_index: edge: 0, circle: 1, text: 3, key: 5
class GraphNode:
    def __init__(self, value, position_x, position_y, is_music_note=False, node_radius=RADIUS, fill_color=BACKGROUND, stroke_color=GRAY, font_color=GRAY, font_size=VALUE_SIZE, zoom_in_power=1):
        self.font_color = font_color
        self.font_size = font_size
        self.zoom_in_power = zoom_in_power
        self.node_radius = node_radius
        self.fill_color = fill_color
        self.stroke_color = stroke_color
        self.value = value
        self.neighbor2edge = {}
        self.neighbors = []
        self.edges = []
        self.position_x = position_x
        self.position_y = position_y
        self.mobject = None
        self.text_mobject = None
        self.text_mobject_is_showing = True
        self.circle_mobject = None
        self._create_mobject(is_music_note=is_music_note)
        self.key = None
        self.key_string = ''
        self.key_mobject = None
        self.animations = None
        self.rect = None
        self.parent = None  # for Union-Find
        self.children = []  # for Union-Find
        self.is_isolated = True
        self.is_showing = False
        self.label_name = ''
        self.label_mobject = None
        self.min_edge = None

    
    def _create_text_mobject(self, color=None):
        if not color:
            color = self.font_color
        count_digit = len(str(self.value))
        if count_digit >= 3:
            self.font_size = self.font_size - (count_digit - 2) * 5
        return Text(str(self.value), color=color, font=FONT, weight=BOLD, font_size=self.font_size/self.zoom_in_power).set_z_index(7).shift(self.circle_mobject.get_center())
    
    def _create_mobject(self, is_music_note):
        """
        Convert a node to an MObject so that it shows on the canvas
        """
        self.circle_mobject = Circle(radius=self.node_radius/self.zoom_in_power).set_stroke(color=self.stroke_color, width=WIDTH/self.zoom_in_power).set_fill(self.fill_color, opacity=1.0).set_z_index(1).shift(RIGHT * self.position_x + UP * self.position_y)
        if not is_music_note:
            self.text_mobject = self._create_text_mobject()
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
        if self.text_mobject_is_showing:
            m["t"] = self.text_mobject
        if self.key_mobject:
            m["k"] = self.key_mobject
        if self.label_mobject:
            m["l"] = self.label_mobject
        return m

    def _update_mobject(self):
        self.mobject = self.mobjects()

    def initialize_key(self, key_string=None, show_value=False, color=GRAY):
        animations = []
        if key_string == '∞':
            self.key = float('inf')
        elif isinstance(key_string, int) or isinstance(key_string, float):
            self.key = key_string
            key_string = str(key_string)
        if show_value:
            new_text_mobject = None
            if show_value == 'BACK':
                new_text_mobject = get_text(str(self.value), NODE_NAME_BACKGROUND_SIZE, color=NODE_NAME_BACKGROUND_COLOR, weight=NODE_NAME_BACKGROUND_WEIGHT).move_to(self.mobject.get_center()).set_fill(opacity=NODE_NAME_BACKGROUND_OPACITY).set_z_index(3)
            if show_value == 'TOP':
                new_text_mobject = get_text(str(self.value), SMALL_FONT_SIZE, color=GRAY, weight=BOLD).next_to(self.mobject, UP, buff=0.15)
            animations.append(ReplacementTransform(self.text_mobject, new_text_mobject))
            self.text_mobject = new_text_mobject
            self.key_mobject = get_text(key_string, font_size=KEY_SIZE, weight=BOLD, color=color).move_to(self.circle_mobject.get_center()).set_z_index(5)
            animations.append(FadeIn(self.key_mobject))
        else:
            self.text_mobject_is_showing = False
            self.key_mobject = get_text(key_string, font_size=KEY_SIZE, weight=BOLD, color=color).move_to(self.circle_mobject.get_center()).set_z_index(5)
            animations.append(ReplacementTransform(self.text_mobject, self.key_mobject))
            self.text_mobject = None
        self._update_mobject()
        self.animations = animations    # If show_value is True, there will be 2 animations: Transform and FadeIn; Otherwise, only 1 animation
        self.key_string = key_string
        return AnimationGroup(*animations, lag_ratio=1)

    def delete_key(self):
        self.key_string = ''
        self.key = None
        return FadeOut(self.key_mobject)

    def fade_out_key_restore_name(self, color=GRAY):
        self.key_string = ''
        self.key = None
        self.text_mobject_is_showing = True
        self.text_mobject = self._create_text_mobject(color)
        return ReplacementTransform(self.key_mobject, self.text_mobject)
    
    def update_key(self, key, color=GRAY):
        animations = []
        new_key_mobject = get_text(str(key), font_size=KEY_SIZE, weight=BOLD, color=color).move_to(self.circle_mobject.get_center()).set_z_index(5)
        animations.append(ReplacementTransform(self.key_mobject, new_key_mobject))
        self.key = key
        self.key_string = str(key)
        self.key_mobject = new_key_mobject
        self.animations = animations
        return AnimationGroup(*animations)
        
    def highlight_stroke(self, color=HIGHLIGHT_STROKE):
        """
        Change the stroke color of the node to be highlight color
        """
        return AnimationGroup(
            self.circle_mobject.animate.set_stroke(color=color), 
            Wait()
        )

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
        return AnimationGroup(
            self.circle_mobject.animate.set_fill(PINK1).set_stroke(PINK2), 
            self.text_mobject.animate.set_color(BACKGROUND)
        )

    def color(self, fill_color=PINK2, stroke_color=PINK3, stroke_width=WIDTH, text_color=BACKGROUND, has_key=False):
        """
        Fill this node as PINK (light pink)
        """
        if not has_key:
            return AnimationGroup(self.circle_mobject.animate.set_fill(fill_color).set_stroke(stroke_color, width=stroke_width), self.text_mobject.animate.set_color(text_color))
        elif self.text_mobject_is_showing:
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
        return FadeIn(self.mobject)

    def fade_in_label(self, label_name, show_background=True, direction='UP', stroke_width=2, font_size=WEIGHT_SIZE, font_weight=NORMAL):
        text = Text(label_name, color=GRAY, font=FONT, weight=font_weight, font_size=font_size).set_z_index(10).set_stroke(color=EDGE_STROKE_COLOR, width=EDGE_STROKE_WIDTH)
        if direction == 'UP':
            text.move_to(self.circle_mobject.get_top()).shift(UP * 0.22)
        elif direction == 'LEFT':
            text.move_to(self.circle_mobject.get_left()).shift(LEFT * 0.22)
        elif direction == 'RIGHT':
            text.move_to(self.circle_mobject.get_right()).shift(RIGHT * 0.22)
        elif direction == 'DOWN':
            text.move_to(self.circle_mobject.get_bottom()).shift(DOWN * 0.22)
        side_length = LABEL_SQUARE_SIZE
        text_background = RoundedRectangle(corner_radius=0.05, width=side_length, height=side_length).set_stroke(color=GRAY, width=stroke_width).set_fill(BACKGROUND, opacity=1.0).set_z_index(9).move_to(text.get_center())
        self.label_name = label_name
        if show_background:
            self.label_mobject = VDict([("text", text), ("text_background", text_background)])
        else:
            self.label_mobject = VDict([("text", text)])
        return FadeIn(self.label_mobject)

    def fade_out_label(self):
        return FadeOut(self.label_mobject)

class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        node = GraphNode(value='A', position_x=1, position_y=1)
        self.play(node.fade_in())
        # self.play(node.initialize_key('∞'))
        # self.wait()
        # self.play(node.update_key('1'))
        # self.wait()
        # self.play(node.fade_out_key_restore_name(color=PINK3))
        # self.wait()