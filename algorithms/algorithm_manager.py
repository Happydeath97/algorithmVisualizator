from typing import List
from map_class import Map
from algorithms.breadth_first_search import BreadthFirstSearch
from algorithms.dijkstra_algorithm import DijkstraAlgorithm
from algorithms.depth_first_search import DepthFirstSearch
from algorithms.random_walk import RandomWalk
from algorithms.astar_shortest_path import Astar


class AlgorithmManager:
    START_SYMBOL = Map.START_SYMBOL
    END_SYMBOL = Map.END_SYMBOL
    WALL_SYMBOL = Map.WALL_SYMBOL
    PATH_SYMBOL = Map.PATH_SYMBOL
    VISITED_SYMBOL = Map.VISITED_SYMBOL
    SOLUTION_SYMBOL = Map.SOLUTION_SYMBOL

    def __init__(self):
        self.algorithms = {
            'bfs': BreadthFirstSearch,
            'astar': Astar,
            'dfs': DepthFirstSearch,
            'dijkstra': DijkstraAlgorithm,
            'random': RandomWalk
        }
        self.selected_algorithm = None
        self.path_generator = iter([])

    def select_algorithm(self, algorithm_name: str):
        if algorithm_name.lower() in self.algorithms:
            self.selected_algorithm = self.algorithms[algorithm_name.lower()]
        else:
            # TODO handle error
            return

    def find_path(self, labyrinth_map: List[List[str]]):
        if not self.selected_algorithm:
            # TODO handle error
            return
        self.selected_algorithm = self.selected_algorithm(labyrinth_map,
                                                          Map.START_SYMBOL,
                                                          Map.END_SYMBOL,
                                                          Map.WALL_SYMBOL)
        self.path_generator = self.selected_algorithm.find_path()

    def give_solution(self):
        if not self.selected_algorithm:
            # TODO handle error
            return
        return self.selected_algorithm.solution
