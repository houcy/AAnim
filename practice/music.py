import pygame.midi
import time
from music_constants import *
from style import *

class Music:
    def __init__(self):
        self.player = None

    def init_midi_play(self):
        pygame.midi.init()
        self.player = pygame.midi.Output(0)
        self.player.set_instrument(0)
    
    def play(self, note, velocity=127, remain_time=1):
        self.player.note_on(note, 127)
        time.sleep(remain_time)
        self.player.note_off(note, 127)

    def destroy(self):
        del self.player
        pygame.midi.quit()


def generate_positions(notes, fit_full_screen=False, buff=NODE_BUFF):
    # notes = NOTES_ORDER[NOTES_ORDER.index(start_note):NOTES_ORDER.index(end_note)+1]
    positions = {}
    if fit_full_screen:
        full_width_screen = 10
        offset = - full_width_screen / 2
        step_length = full_width_screen / (len(notes) - 1)
        for i, note in enumerate(notes):
            position_x = i * step_length + offset
            positions[note] = (position_x, 0)
        return positions
    else:
        n = len(notes)
        if n % 2 == 1:
            mid = n // 2
            for i, note in enumerate(notes):
                position_x = (i - mid) * buff
                positions[note] = (position_x, 0)
        else:
            mid = n // 2 - 1
            for i, note in enumerate(notes):
                position_x = (i - mid) * buff - buff / 2
                positions[note] = (position_x, 0)
        return positions

