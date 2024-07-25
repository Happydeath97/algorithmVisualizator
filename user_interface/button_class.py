from typing import Tuple
from pygame import Surface, draw, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.font import Font


class Button:
    def __init__(self, start_pos: Tuple[int, int], size: Tuple[int, int], name: str):
        self.pos = start_pos
        self.size = size
        self.active = False
        self.pressed = False
        self.name = name

    def draw_text(self, sc: Surface, text: str, font_size: int = 24, color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        font = Font(None, font_size)
        text_surface = font.render(text, True, color)
        sc.blit(text_surface, (self.pos[0] + self.size[0]/2 - font.size(text)[0]/2,
                               self.pos[1] + self.size[1]/2 - font.size(text)[1]/2
                               ))

    def draw(self, sc: Surface) -> None:
        if not self.pressed:
            color = (100, 150, 150)
        else:
            color = (150, 100, 150)

        draw.rect(sc, color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        self.draw_text(sc, f"{self.name}")

    def handle(self, event) -> None:
        if event.type == MOUSEBUTTONDOWN:
            if self.pos[0] <= event.pos[0] <= self.pos[0] + self.size[0] and \
                    self.pos[1] <= event.pos[1] <= self.pos[1] + self.size[1]:

                self.pressed = True

        elif event.type == MOUSEBUTTONUP:
            if self.pressed:
                if self.pos[0] <= event.pos[0] <= self.pos[0] + self.size[0] and self.pos[1] <= event.pos[1] <= \
                        self.pos[1] + self.size[1]:
                    print(f"Button {self.name} pressed!")
                self.pressed = False
