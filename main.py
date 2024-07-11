import pygame
import time

from MapClass import Map
from SliderClass import Slider
from GameState import StateManager, GameState
from KeyHandlerClass import KeyHandler
from algorithms.BreadthFirstSearch import BreadthFirstSearch

# pygame setup
pygame.init()
SCREEN_W, SCREEN_H = 1280, 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Path Finding Visualization")
clock = pygame.time.Clock()
RUNNING = True
ALGORITHM = None
dt_ups = 0
dt_fps = 0
UPS = 200
time_per_update = int(1000 / UPS)
FPS = 60
time_per_frame = int(1000 / FPS)

TILE_SIZE = 10
START_POS_MAP = (300, 50)
END_POS_MAP = (950, 500)
######################################################################################
SLIDER_X, SLIDER_Y = 20, 100
SLIDER_WIDTH, SLIDER_HEIGHT = 80, 10
KNOB_RADIUS = 5
MIN_VAL, MAX_VAL = 10, 40


def draw_screen(sc: pygame.Surface, state_m: StateManager, map_maze: Map, map_size: Slider) -> None:
    global ALGORITHM
    sc.fill((200, 200, 200))
    if state_m.get_state() == GameState.EDITING:
        map_maze.draw(sc)
        map_size.draw(sc)

    elif state_m.get_state() == GameState.VISUALIZATING:
        map_maze.draw(sc)
        map_size.draw(sc)

        if not ALGORITHM:
            ALGORITHM = BreadthFirstSearch(map_maze.map, Map.START_SYMBOL, Map.END_SYMBOL, Map.WALL_SYMBOL)
        for coord in ALGORITHM.find_path():
            map_maze.visit_place_on_map(coord, sc)
            pygame.time.delay(10)

        map_maze.show_solution(ALGORITHM.solution, sc)
        pygame.time.delay(3000)
        ALGORITHM = None
        state_m.change_state(GameState.EDITING)

    elif state_m.get_state() == GameState.MENU:
        pass
    pygame.display.flip()


def update(state_m: StateManager, map_maze: Map, map_size: Slider) -> None:
    global RUNNING, ALGORITHM

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if state_m.get_state() == GameState.EDITING:
            map_size.handle(event)

    if state_m.get_state() == GameState.EDITING:
        map_maze.resize_map(map_size.val)
        map_maze.handle()
        if key_handler.is_key_pressed(pygame.K_ESCAPE):
            state_m.change_state(GameState.MENU)
        if key_handler.is_key_pressed(pygame.K_RETURN):
            state_m.change_state(GameState.VISUALIZATING)

    elif state_m.get_state() == GameState.VISUALIZATING:
        pass

    elif state_m.get_state() == GameState.MENU:
        if key_handler.is_key_pressed(pygame.K_ESCAPE):
            state_m.change_state(GameState.EDITING)


if __name__ == "__main__":
    state_manager = StateManager()
    key_handler = KeyHandler(debounce_time=0.2)
    m = Map(TILE_SIZE, START_POS_MAP, END_POS_MAP)
    map_size_slider = Slider((SLIDER_X, 100), (SLIDER_WIDTH, SLIDER_HEIGHT), KNOB_RADIUS, (MIN_VAL, MAX_VAL), "Test")
    while RUNNING:
        dt = clock.tick()

        dt_ups += dt
        dt_fps += dt

        if dt_fps >= time_per_frame:
            dt_fps = 0

            draw_screen(screen, state_manager, m, map_size_slider)

        if dt_ups >= time_per_update:
            dt_ups = 0
            update(state_manager, m, map_size_slider)

    pygame.quit()
    quit()
