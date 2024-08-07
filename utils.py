from user_interface.button_class import ButtonGroup
from map_class import Map
from pygame import Surface
from pygame.font import Font
from typing import Tuple


def render_about(sc: Surface, font_size: int, color: Tuple[int, int, int] = (0, 0, 0)) -> None:
    font = Font(None, font_size)
    text = """
    Tohle je test textu jak zobrazit
    ostatni text a poslat blabla
    lorem ipsum mit dollor
    tohle je text ahhahaha
    """
    lines = text.split('\n')
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        sc.blit(text_surface, (0, 0 + i * font.get_linesize()))


def get_current_path_symbol(button_group: ButtonGroup) -> str:
    for button in button_group.buttons:
        if not button.active:
            continue
        elif button.name.lower() == "path":
            return Map.PATH_SYMBOL
        elif button.name.lower() == "start":
            return Map.START_SYMBOL
        elif button.name.lower() == "end":
            return Map.END_SYMBOL
        else:
            return Map.PATH_SYMBOL


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
