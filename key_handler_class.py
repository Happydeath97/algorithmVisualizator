import pygame
import time


class KeyHandler:
    def __init__(self, debounce_time=0.2):
        self.key_states = {}
        self.debounce_time = debounce_time
        self.last_pressed_time = {}

    def is_key_pressed(self, key):
        keys = pygame.key.get_pressed()
        current_time = time.time()

        if key not in self.key_states:
            self.key_states[key] = False
            self.last_pressed_time[key] = 0

        if keys[key]:
            if not self.key_states[key] and (current_time - self.last_pressed_time[key] > self.debounce_time):
                self.key_states[key] = True
                self.last_pressed_time[key] = current_time
                return True
        else:
            self.key_states[key] = False

        return False
