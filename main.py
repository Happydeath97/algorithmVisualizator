import pygame

from map_class import Map
from user_interface.slider_class import Slider
from user_interface.button_class import Button, ButtonGroup
from game_state import StateManager, GameState
from key_handler_class import KeyHandler
from algorithms.algorithm_manager import AlgorithmManager

# pygame setup
pygame.init()
SCREEN_W, SCREEN_H = 1280, 720
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Path Finding Visualization")
clock = pygame.time.Clock()
RUNNING = True
ALGORITHM = AlgorithmManager()
dt_ups = 0
dt_fps = 0
UPS = 200
time_per_update = int(1000 / UPS)
FPS = 120
time_per_frame = int(1000 / FPS)

TILE_SIZE = 10
START_POS_MAP = (300, 50)
END_POS_MAP = (950, 500)
######################################################################################
SLIDER_X, SLIDER_Y = 20, 100
SLIDER_WIDTH, SLIDER_HEIGHT = 80, 10
KNOB_RADIUS = 5
MIN_VAL, MAX_VAL = 10, 40


def draw_screen(sc: pygame.Surface, state_m: StateManager, map_maze: Map,
                map_size: Slider, alg_speed: Slider, alg_group_b: ButtonGroup, gen_b_group) -> None:
    global ALGORITHM

    if state_m.get_state() == GameState.EDITING:
        sc.fill((200, 200, 200))
        map_maze.draw(sc)
        map_size.draw(sc)
        alg_speed.draw(sc)
        alg_group_b.draw(sc)
        gen_b_group.draw(sc)

    elif state_m.get_state() == GameState.VISUALIZATING:
        # TODO encapsulate this:
        if not ALGORITHM.selected_algorithm:
            selected_algorithm = get_current_algorithm(alg_group_b)
            ALGORITHM.select_algorithm(selected_algorithm)
            ALGORITHM.find_path(map_maze.map)

        if ALGORITHM.selected_algorithm:
            coord = next(ALGORITHM.path_generator, None)
            if coord:
                map_maze.visit_place_on_map(coord, sc)
                pygame.time.delay(100 - alg_speed.val*10)
            else:
                map_maze.show_solution(ALGORITHM.give_solution(), sc)
                pygame.time.delay(3000)
                ALGORITHM = AlgorithmManager()
                state_m.change_state(GameState.EDITING)
        else:
            state_m.change_state(GameState.EDITING)

    elif state_m.get_state() == GameState.MENU:
        sc.fill((200, 200, 200))
        pass
    pygame.display.flip()


def update(state_m: StateManager, map_maze: Map, map_size: Slider, alg_speed: Slider, alg_group_b: ButtonGroup, gen_b_group) -> None:
    global RUNNING, ALGORITHM

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if state_m.get_state() == GameState.EDITING:
            # handle sliders
            map_size.handle(event)
            alg_speed.handle(event)
            alg_group_b.handle(event)
            gen_b_group.handle(event)

        elif state_m.get_state() == GameState.VISUALIZATING:
            pass
        elif state_m.get_state() == GameState.MENU:
            pass

    # game state specific actions that don't need to check events (do not need to be called for each event)
    if state_m.get_state() == GameState.EDITING:
        map_maze.resize_map(map_size.val)
        map_maze.handle()
        if key_handler.is_key_pressed(pygame.K_ESCAPE):
            state_m.change_state(GameState.MENU)
        if key_handler.is_key_pressed(pygame.K_RETURN) and map_maze.ready():
            state_m.change_state(GameState.VISUALIZATING)

        # TODO: Instead of changing this with a key button change it with a button in the app
        #  (implement buttons in interface)
        if key_handler.is_key_pressed(pygame.K_a):
            map_maze.change_current_symbol(Map.PATH_SYMBOL)
        if key_handler.is_key_pressed(pygame.K_s):
            map_maze.change_current_symbol(Map.START_SYMBOL)
        if key_handler.is_key_pressed(pygame.K_d):
            map_maze.change_current_symbol(Map.END_SYMBOL)
        # if key_handler.is_key_pressed(pygame.K_r):
        if gen_b_group.at_least_one_member_active():
            map_maze.generate_maze()
            gen_b_group.set_all_inactive()

    elif state_m.get_state() == GameState.VISUALIZATING:
        pass

    elif state_m.get_state() == GameState.MENU:
        if key_handler.is_key_pressed(pygame.K_ESCAPE):
            state_m.change_state(GameState.EDITING)


def get_current_algorithm(alg_group_b: ButtonGroup) -> str:
    for button in alg_group_b.buttons:
        if not button.active:
            continue
        if button.name == "A*":
            return "astar"
        elif button.name == "BFS":
            return "bfs"
        elif button.name == "DFS":
            return "dfs"
        elif button.name == "Dijkstra":
            return "dijkstra"
        elif button.name == "Random Walk":
            return "random"
        else:
            return "bfs"


if __name__ == "__main__":
    state_manager = StateManager()
    key_handler = KeyHandler(debounce_time=0.2)
    m = Map(TILE_SIZE, START_POS_MAP, END_POS_MAP)
    map_size_slider = Slider((SLIDER_X, 100), (SLIDER_WIDTH, SLIDER_HEIGHT), KNOB_RADIUS, (MIN_VAL, MAX_VAL),
                             "Tile Size")
    alg_speed_slider = Slider((SLIDER_X, 200), (SLIDER_WIDTH, SLIDER_HEIGHT), KNOB_RADIUS, (1, 10), "Speed")

    astar_b = Button((SCREEN_W - 145, 100), (95, 50), "A*")
    bfs_b = Button((SCREEN_W - 250, 100), (95, 50), "BFS")
    dijkstra_b = Button((SCREEN_W - 145, 160), (95, 50), "Dijkstra")
    dfs_b = Button((SCREEN_W - 250, 160), (95, 50), "DFS")
    random_b = Button((SCREEN_W - 250, 220), (200, 50), "Random Walk")
    alg_button_group = ButtonGroup(astar_b, bfs_b, dfs_b, dijkstra_b, random_b)

    generate_b = Button((SCREEN_W - 250, 290), (200, 50), "Generate Maze")
    gen_b_group = ButtonGroup(generate_b)

    while RUNNING:
        dt = clock.tick()

        dt_ups += dt
        dt_fps += dt

        if dt_ups >= time_per_update:
            dt_ups = 0
            update(state_manager, m, map_size_slider, alg_speed_slider, alg_button_group, gen_b_group)

        if dt_fps >= time_per_frame:
            dt_fps = 0

            # TODO in future make all interface parts (slider etc) in a list or something
            draw_screen(screen, state_manager, m, map_size_slider, alg_speed_slider, alg_button_group, gen_b_group)

    pygame.quit()
    quit()
