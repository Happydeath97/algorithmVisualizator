from typing import Tuple
from pygame import Surface, draw, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.font import Font


class Button:
    def __init__(self, start_pos: Tuple[int, int], size: Tuple[int, int], name: str, font_size: int = 24):
        self.pos = start_pos
        self.size = size
        self.active = False
        self.pressed = False
        self.name = name
        self.font_size = font_size

    def draw_text(self, sc: Surface, text: str, color: Tuple[int, int, int] = (0, 0, 0)) -> None:
        font = Font(None, self.font_size)
        text_surface = font.render(text, True, color)
        sc.blit(text_surface, (self.pos[0] + self.size[0]/2 - font.size(text)[0]/2,
                               self.pos[1] + self.size[1]/2 - font.size(text)[1]/2
                               ))

    def draw(self, sc: Surface) -> None:
        color = (150, 150, 100) if self.active else (150, 100, 150)
        color = (100, 150, 150) if self.pressed else color

        draw.rect(sc, color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        self.draw_text(sc, f"{self.name}")

    def handle(self, event, button_group) -> None:
        if event.type == MOUSEBUTTONDOWN:
            if self.pos[0] <= event.pos[0] <= self.pos[0] + self.size[0] and \
                    self.pos[1] <= event.pos[1] <= self.pos[1] + self.size[1]:

                self.pressed = True

        elif event.type == MOUSEBUTTONUP:
            if self.pressed:
                if self.pos[0] <= event.pos[0] <= self.pos[0] + self.size[0] and self.pos[1] <= event.pos[1] <= \
                        self.pos[1] + self.size[1]:
                    button_group.set_active(self)
                self.pressed = False


class ButtonGroup:
    def __init__(self, *buttons: Button):
        self.buttons = list(buttons)
        self.buttons[0].active = True

    def add_button(self, button: Button) -> None:
        self.buttons.append(button)

    def set_active(self, active_button: Button) -> None:
        for button in self.buttons:
            button.active = (button == active_button)

    def at_least_one_member_active(self) -> bool:
        if any(button.active for button in self.buttons):
            return True
        return False

    def set_all_inactive(self) -> None:
        for button in self.buttons:
            button.active = False

    def handle(self, event) -> None:
        for button in self.buttons:
            button.handle(event, self)

    def draw(self, sc: Surface) -> None:
        for button in self.buttons:
            button.draw(sc)
