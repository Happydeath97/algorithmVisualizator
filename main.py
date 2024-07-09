import pygame
from pygame import Surface
import time

import map
from map import Map

# pygame setup
pygame.init()
pygame.display.set_caption("Jump Game")
SCREEN_W, SCREEN_H = 1280, 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
running = True
dt_ups = 0
dt_fps = 0
UPS = 200
time_per_update = int(1000 / UPS)
FPS = 60
time_per_frame = int(1000 / FPS)

TILE_SIZE = 37
START_POS_MAP = (300, 50)
END_POS_MAP = (950, 500)
m = Map(TILE_SIZE, START_POS_MAP, END_POS_MAP)
######################################################################################
SLIDER_X, SLIDER_Y = 20, 100
SLIDER_WIDTH, SLIDER_HEIGHT = 80, 10
KNOB_RADIUS = 5
MIN_VAL, MAX_VAL = 10, 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
BLUE = (0, 0, 255)
slider_val = MIN_VAL
dragging = False


def draw_text(surface, text, position, font_size=24, color=BLACK):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


def draw_slider(val):

    # Draw the slider track
    pygame.draw.rect(screen, GREY, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))

    # Calculate knob position
    knob_x = SLIDER_X + (val - MIN_VAL) / (MAX_VAL - MIN_VAL) * SLIDER_WIDTH
    knob_y = SLIDER_Y + SLIDER_HEIGHT // 2

    # Draw the knob
    pygame.draw.circle(screen, BLUE, (int(knob_x), knob_y), KNOB_RADIUS)

    # Draw the value text
    draw_text(screen, f"Tile Size: {val}", (SLIDER_X, SLIDER_Y - 40))


def get_slider_value(mouse_x):
    # Calculate the value based on the knob position
    ratio = (mouse_x - SLIDER_X) / SLIDER_WIDTH
    value = MIN_VAL + ratio * (MAX_VAL - MIN_VAL)
    return max(MIN_VAL, min(MAX_VAL, int(value)))


def draw_screen(sc: Surface) -> None:
    sc.fill((200, 200, 200))
    m.draw_map(sc)
    draw_slider(slider_val)
    pygame.display.flip()


def update() -> None:
    m.resize_map(slider_val)
    m.update_map()


if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                knob_x = SLIDER_X + (slider_val - MIN_VAL) / (MAX_VAL - MIN_VAL) * SLIDER_WIDTH
                if (knob_x - KNOB_RADIUS <= mouse_x <= knob_x + KNOB_RADIUS and
                        SLIDER_Y - KNOB_RADIUS <= mouse_y <= SLIDER_Y + SLIDER_HEIGHT + KNOB_RADIUS):
                    dragging = True

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = event.pos
                    slider_val = get_slider_value(mouse_x)



        dt = clock.tick()

        dt_ups += dt
        dt_fps += dt

        if dt_fps >= time_per_frame:
            dt_fps = 0

            draw_screen(screen)

        if dt_ups >= time_per_update:
            dt_ups = 0
            update()

    pygame.quit()
    quit()
