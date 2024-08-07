from user_interface.button_class import ButtonGroup
from map_class import Map


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
