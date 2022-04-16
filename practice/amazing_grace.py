from manim import *
from style import *
from code_constant import *
from graph import GraphObject
from music import Music
from music_constants import *
from code_block import CodeBlock
from legend import Legend
from graph_edges_group import GraphEdgesGroup
from graph_nodes_group import GraphNodesGroup
from util import *
from scale_position import *
from union_find import UnionFind
import copy
from collections import defaultdict
import pygame.midi
from straight_graph import StraightGraph


POSITION = {'G3': (-2, 0), 'C4': (0, 0), 'A3': (-1, -1), 'D4': (1, 1), 'E4': (1, -1), 'G4': (2, 0)}
ADJACENCY_LIST = {'C4': {'E4': None, 'A3': None, 'G3': None, 'C4': None}, 'E4': {'C4': None, 'D4': None, 'G4': None}, 'D4': {'C4': None, 'G4': None}, 'G3': {'C4': None, 'A3': None, 'G3': None}, 'G4': {'E4': None}, 'A3': {'C4': None, 'G3': None}}
G_NOTES = [
    ('G3', 1), ('C4', 2), ('E4', 0.5), ('C4', 0.5), ('E4', 2), ('D4', 1), ('C4', 2), ('A3', 1), ('G3', 2), 
    # ('G3', 1), ('C4', 2), ('E4', 0.5), ('C4', 0.5), ('E4', 2), ('D4', 1), ('G4', 5), 
    # ('E4', 1), ('G4', 1.5), ('E4', 0.5), ('G4', 0.5), ('E4', 0.5), ('C4', 2), 
    # ('G3', 1), ('A3', 1.5), ('C4', 0.5), ('C4', 0.5), ('A3', 0.5), ('G3', 2), 
    # ('G3', 1), ('C4', 2), ('E4', 0.5), ('C4', 0.5), ('E4', 2), ('D4', 1), ('C4', 3)
]

ALL_NOTES = ['B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6', 'D6', 'E6', 'F6']
D4_ADJACENCY_LIST = {'G4': {'B4': None, 'E4': None, 'D4': None, 'G4': None}, 'B4': {'G4': None, 'A4': None, 'D5': None}, 'A4': {'G4': None, 'D5': None}, 'D4': {'G4': None, 'E4': None, 'D4': None}, 'D5': {'B4': None}, 'E4': {'G4': None, 'D4': None}}
D4_NOTES = [
    ('D4', 1), ('G4', 2), ('B4', 0.5), ('G4', 0.5), ('B4', 2), ('A4', 1), ('G4', 2), ('E4', 1), ('D4', 2), 
    ('D4', 1), ('G4', 2), ('B4', 0.5), ('G4', 0.5), ('B4', 2), ('A4', 1), ('D5', 5), 
    ('B4', 1), ('D5', 1.5), ('B4', 0.5), ('D5', 0.5), ('B4', 0.5), ('G4', 2), 
    ('D4', 1), ('E4', 1.5), ('G4', 0.5), ('G4', 0.5), ('E4', 0.5), ('D4', 2), 
    ('D4', 1), ('G4', 2), ('B4', 0.5), ('G4', 0.5), ('B4', 2), ('A4', 1), ('G4', 3)
]

D5_NOTES = [
    ('D5', 1), ('G5', 2), ('B5', 0.5), ('G5', 0.5), ('B5', 2), ('A5', 1), ('G5', 2), ('E5', 1), ('D5', 2), 
    ('D5', 1), ('G5', 2), ('B5', 0.5), ('G5', 0.5), ('B5', 2), ('A5', 1), ('D6', 5), 
    ('B5', 1), ('D6', 1.5), ('B5', 0.5), ('D6', 0.5), ('B5', 0.5), ('G5', 2), 
    ('D5', 1), ('E5', 1.5), ('G5', 0.5), ('G5', 0.5), ('E5', 0.5), ('D5', 2), 
    ('D5', 1), ('G5', 2), ('B5', 0.5), ('G5', 0.5), ('B5', 2), ('A5', 1), ('G5', 3)
]

SONG_ADJACENCY_LIST = {'G4': {'B4': None, 'E4': None, 'D4': None, 'G4': None}, 'B4': {'G4': None, 'A4': None, 'D5': None}, 'A4': {'G4': None, 'D5': None}, 'D4': {'G4': None, 'E4': None, 'D4': None}, 'D5': {'B4': None, 'G5': None, 'E5': None, 'D5': None}, 'E4': {'G4': None, 'D4': None}, 'G5': {'B5': None, 'E5': None, 'D5': None, 'G5': None}, 'B5': {'G5': None, 'A5': None, 'D6': None}, 'A5': {'G5': None, 'D6': None}, 'D6': {'B5': None}, 'E5': {'G5': None, 'D5': None}}


##############


PINKS = [GRAY, '#EDC0E8', '#E298D9', '#D770CA', '#CB49BC', '#AF32A1']
SPEED = 0.1

class Show(Scene):
    def construct(self):
        def opening(music_graph, music=None):
            node_names = music_graph.get_node_names()
            for note_name in ['G3', 'A3', 'C4', 'D4', 'E4', 'G4']:
                if note_name in node_names:
                    filename = str(NOTE_TO_MIDI[note_name]) + "-1" + ".wav"
                    self.play(FadeIn(music_graph.value2node[note_name].mobject), run_time=0.1)
                    music.player.note_on(NOTE_TO_MIDI[note_name], VOL)
                    music.player.note_off(NOTE_TO_MIDI[note_name], VOL)
                    self.add_sound(filename)
                    self.wait()
                    self.play(FadeOut(music_graph.value2node[note_name].mobject), run_time=0.5)

        def play(music_graph, notes, colors, speed, player):
            i = 0
            last_animation = None
            while i < len(notes):
                note_name, note_duration = notes[i]
                player.note_on(NOTE_TO_MIDI[note_name], VOL)
                player.note_off(NOTE_TO_MIDI[note_name], VOL)
                # filename = str(NOTE_TO_MIDI[note_name]) + "-" + str(note_duration) + ".wav"
                # print(filename)
                # self.add_sound(filename)
                self.play(music_graph.highlight(note_name, fill_color=BACKGROUND, stroke_color=PINK5, text_color=GRAY), run_time=speed)
                node = music_graph.value2node[note_name]
                edge = None
                color_index = 0
                if i < len(notes) - 1:
                    next_note, _ = notes[i+1]
                    next_node = music_graph.value2node[next_note]
                    edge = music_graph.get_edge(node, next_node)
                    color_index = edge.visit_count
                    if color_index >= len(colors):
                        color_index = len(colors) - 1
                    if edge.visit_count == 0:
                        if last_animation:
                            self.play(music_graph.highlight(note_name, fill_color=PINK4, stroke_color=PINK5), last_animation, run_time=note_duration)
                        else:
                            self.play(music_graph.highlight(note_name, fill_color=PINK4, stroke_color=PINK5), run_time=note_duration)
                        self.play(music_graph.highlight(note_name, fill_color=BACKGROUND, stroke_color=GRAY, text_color=GRAY), run_time=speed)
                        last_animation = edge.fade_in()
                    else:
                        if last_animation:
                            self.play(music_graph.highlight(note_name, fill_color=PINK4, stroke_color=PINK5), last_animation, run_time=note_duration)
                        else:
                            self.play(music_graph.highlight(note_name, fill_color=PINK4, stroke_color=PINK5), run_time=note_duration)
                        self.play(music_graph.highlight(note_name, fill_color=BACKGROUND, stroke_color=GRAY, text_color=GRAY), run_time=speed)
                        last_animation = edge.highlight(color=colors[color_index], width=WIDTH+edge.visit_count/2, change_tip_width=True)
                    edge.visit_count += 1
                else:
                    # last node
                    if last_animation:
                        self.play(music_graph.highlight(note_name, fill_color=PINK4, stroke_color=PINK5), last_animation, run_time=note_duration)
                    else:
                        elf.play(music_graph.highlight(note_name, fill_color=PINK4, stroke_color=PINK5), run_time=note_duration)
                    self.play(music_graph.highlight(note_name, fill_color=BACKGROUND, stroke_color=GRAY, text_color=GRAY), run_time=speed)
                i += 1

        self.camera.background_color = BACKGROUND
        w = watermark()
        self.add(w)
        pygame.midi.init()
        player = pygame.midi.Output(0)
        player.set_instrument(0)

        music_graph_inline = StraightGraph(SONG_ADJACENCY_LIST, ALL_NOTES, is_music_note=True)

        self.play(music_graph_inline.show('D5', 'D6'))
        play(music_graph_inline, D5_NOTES, PINKS, SPEED, player)
        self.play(music_graph_inline.hide_all_edges())

        self.play(music_graph_inline.show_all_hidden_nodes())
        self.play(music_graph_inline.shift('D4', 'D5'))
        self.play(music_graph_inline.hide_nodes_not_in('D4', 'D5'))
        play(music_graph_inline, D4_NOTES, PINKS, SPEED, player)
        self.wait(10)
        