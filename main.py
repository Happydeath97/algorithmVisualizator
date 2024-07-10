import pygame

from MapClass import Map
from SliderClass import Slider

# pygame setup
pygame.init()
pygame.display.set_caption("Jump Game")
SCREEN_W, SCREEN_H = 1280, 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
RUNNING = True
dt_ups = 0
dt_fps = 0
UPS = 200
time_per_update = int(1000 / UPS)
FPS = 60
time_per_frame = int(1000 / FPS)

TILE_SIZE = 37
START_POS_MAP = (300, 50)
END_POS_MAP = (950, 500)
######################################################################################
SLIDER_X, SLIDER_Y = 20, 100
SLIDER_WIDTH, SLIDER_HEIGHT = 80, 10
KNOB_RADIUS = 5
MIN_VAL, MAX_VAL = 10, 40


def draw_screen(sc: pygame.Surface, *args) -> None:
    sc.fill((200, 200, 200))
    for obj in args:
        obj.draw(sc)
    pygame.display.flip()


def update(map_maze: Map, map_size: Slider) -> None:
    global RUNNING
    for event in pygame.event.get():
        map_size.handle(event)
        if event.type == pygame.QUIT:
            RUNNING = False
    map_maze.resize_map(map_size.val)
    map_maze.handle()


if __name__ == "__main__":
    m = Map(TILE_SIZE, START_POS_MAP, END_POS_MAP)
    map_size_slider = Slider((SLIDER_X, 100), (SLIDER_WIDTH, SLIDER_HEIGHT), KNOB_RADIUS, (MIN_VAL, MAX_VAL), "Test")
    while RUNNING:
        dt = clock.tick()

        dt_ups += dt
        dt_fps += dt

        if dt_fps >= time_per_frame:
            dt_fps = 0

            draw_screen(screen, m, map_size_slider)

        if dt_ups >= time_per_update:
            dt_ups = 0
            update(m, map_size_slider)

    pygame.quit()
    quit()
