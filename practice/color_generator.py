from manim import *
from style import *
import colorsys

class ColorGenerator:
    def __init__(self):
        pass

    def hsv_to_rgb(self, hsv):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(*hsv))

    def rgb_to_hex(self, rgb):
        return '%02x%02x%02x' % rgb
    
    def vivid_colors(self, n):
        s = 0.34
        v = 0.93
        s_low = 0.15
        v_low = 0.93
        offset = 0.5
        step_length = 1 / n
        hsv_colors = []
        stroke_hsv_colors = []
        for i in range(n):
            h = (i * step_length + offset) % 1
            hsv_colors.append((h, s, v))
            stroke_hsv_colors.append((h, s_low, v_low))
        rgb_colors = [self.hsv_to_rgb(color) for color in hsv_colors]
        stroke_rgb_colors = [self.hsv_to_rgb(color) for color in stroke_hsv_colors]
        hex_colors = [self.rgb_to_hex(color) for color in rgb_colors]
        stroke_hex_colors = [self.rgb_to_hex(color) for color in stroke_rgb_colors]
        hex_colors_cor_manim = ["#" + color for color in hex_colors]
        stroke_hex_colors_cor_manim = ["#" + color for color in stroke_hex_colors]
        print("vivid_colors: ", stroke_hex_colors_cor_manim)
        return list(zip(hex_colors_cor_manim, stroke_hex_colors_cor_manim))

class Test(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        cg = ColorGenerator()
        for i in cg.vivid_colors(10):
            self.play(FadeIn(Square().set_fill(color=i, opacity=1)))