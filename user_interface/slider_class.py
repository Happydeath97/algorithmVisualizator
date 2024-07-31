from typing import Tuple
from pygame import Surface, draw, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame.font import Font


class Slider:
    def __init__(self, start_pos: Tuple[int, int], slider_size: Tuple[int, int],
                 slider_range: Tuple[int, int], name: str):
        self.pos = start_pos
        self.slider_size = slider_size
        self.knob_r = slider_size[1] // 2
        self.range = slider_range
        self.val = self.range[0]
        self.dragging = False
        self.name = name

    def draw_text(self, sc: Surface, text: str, font_size: int = 24, color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        font = Font(None, font_size)
        text_surface = font.render(text, True, color)
        sc.blit(text_surface, (self.pos[0], self.pos[1] - 30))

    def draw(self, sc: Surface) -> None:
        # Draw the slider track
        draw.rect(sc, (150, 150, 150), (self.pos[0], self.pos[1], self.slider_size[0], self.slider_size[1]))

        # Calculate knob position
        knob_x = self.pos[0] + (
                self.val - self.range[0]
        ) / (self.range[1] - self.range[0]) * self.slider_size[0]
        knob_y = self.pos[1] + self.slider_size[1] // 2

        # Draw the knob
        draw.circle(sc, (0, 0, 255), (int(knob_x), knob_y), self.knob_r)

        # Draw the value text
        self.draw_text(sc, f"{self.name}: {self.val}")

    def get_slider_value(self, mouse_x: int) -> int:
        # Calculate the value based on the knob position
        ratio = (mouse_x - self.pos[0]) / self.slider_size[0]
        value = self.range[0] + ratio * (self.range[1] - self.range[0])
        return max(self.range[0], min(self.range[1], int(value)))

    def handle(self, event) -> None:
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            knob_x = self.pos[0] + (self.val - self.range[0]) / (self.range[1] - self.range[0]) * self.slider_size[0]
            if (knob_x - self.knob_r <= mouse_x <= knob_x + self.knob_r and
                    self.pos[1] - self.knob_r <= mouse_y <= self.pos[1] + self.slider_size[1] + self.knob_r):
                self.dragging = True

        elif event.type == MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.val = self.get_slider_value(mouse_x)
