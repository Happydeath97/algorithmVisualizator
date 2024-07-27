from typing import Tuple, List
from pygame import Surface, draw, mouse
import pygame
import random


class Map:
    START_SYMBOL = "X"
    END_SYMBOL = "O"
    WALL_SYMBOL = "x"
    PATH_SYMBOL = "#"
    VISITED_SYMBOL = "V"
    SOLUTION_SYMBOL = "S"

    def __init__(self, tile_size: int, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        self.tile_size = tile_size
        self.org_start = start_pos
        self.org_end = end_pos
        self.end_pos = (
            self.org_start[0] + ((self.org_end[0] - self.org_start[0]) // self.tile_size + 1) * self.tile_size,
            self.org_start[1] + ((self.org_end[1] - self.org_start[1]) // self.tile_size + 1) * self.tile_size
        )
        delta_width = (self.end_pos[0] - self.org_end[0]) // 2
        self.start_pos = self.org_start[0] - delta_width, self.org_start[1]
        self.end_pos = self.end_pos[0] - delta_width, self.end_pos[1]
        self.num_of_rows = (self.end_pos[1] - self.start_pos[1]) // self.tile_size
        self.num_of_cols = (self.end_pos[0] - self.start_pos[0]) // self.tile_size
        self.map = [[Map.PATH_SYMBOL for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]
        self.current_symbol = Map.PATH_SYMBOL

    def draw_rows(self, sc: Surface) -> None:
        y = 0

        for _ in range(self.num_of_rows + 1):
            draw.line(sc,
                      (255, 255, 255),
                      (self.start_pos[0], self.start_pos[1] + y),
                      (self.end_pos[0], self.start_pos[1] + y)
                      )
            y += self.tile_size

    def draw_cols(self, sc: Surface) -> None:
        x = 0

        for _ in range(self.num_of_cols + 1):
            draw.line(sc,
                      (255, 255, 255),
                      (self.start_pos[0] + x, self.start_pos[1]),
                      (self.start_pos[0] + x, self.end_pos[1])
                      )

            x += self.tile_size

    def draw(self, sc: Surface) -> None:
        draw.rect(sc, (0, 0, 0), (
            self.start_pos[0],
            self.start_pos[1],
            self.end_pos[0] - self.start_pos[0],
            self.end_pos[1] - self.start_pos[1]
        ))
        self.draw_rows(sc)
        self.draw_cols(sc)

        for row_index, row in enumerate(self.map):
            for col_index, col in enumerate(row):
                x = col_index * self.tile_size + self.start_pos[0]
                y = row_index * self.tile_size + self.start_pos[1]
                if col == Map.PATH_SYMBOL:  # Path
                    draw.rect(sc, (160, 100, 80), (x, y, self.tile_size, self.tile_size))
                elif col == Map.WALL_SYMBOL:  # Wall
                    draw.rect(sc, (110, 110, 110), (x + 1, y + 1, self.tile_size - 2, self.tile_size - 2))
                elif col == Map.END_SYMBOL:
                    draw.rect(sc, (160, 0, 0), (x, y, self.tile_size, self.tile_size))
                elif col == Map.START_SYMBOL:
                    draw.rect(sc, (0, 160, 0), (x, y, self.tile_size, self.tile_size))
                elif col == Map.VISITED_SYMBOL:
                    draw.rect(sc, (61, 90, 254), (x, y, self.tile_size, self.tile_size))
                elif col == Map.SOLUTION_SYMBOL:
                    draw.rect(sc, (144, 202, 249), (x, y, self.tile_size, self.tile_size))

    def handle(self) -> None:
        mouse_buttons = mouse.get_pressed()

        if not any(mouse_buttons):
            return

        x = mouse.get_pos()[0] - self.start_pos[0]
        y = mouse.get_pos()[1] - self.start_pos[1]

        row, column = self.get_map_indexes((x, y))

        if row >= len(self.map) or column >= len(self.map[0]):
            return
        elif row < 0 or column < 0:
            return

        if mouse_buttons[0]:
            if self.current_symbol == Map.PATH_SYMBOL:
                self.map[row][column] = self.current_symbol
            if self.current_symbol == Map.START_SYMBOL:
                self.replace_symbol_in_map(Map.START_SYMBOL, Map.WALL_SYMBOL)
                self.map[row][column] = self.current_symbol
            if self.current_symbol == Map.END_SYMBOL:
                self.replace_symbol_in_map(Map.END_SYMBOL, Map.WALL_SYMBOL)
                self.map[row][column] = self.current_symbol

        elif mouse_buttons[2]:
            self.map[row][column] = Map.WALL_SYMBOL

    def replace_symbol_in_map(self, to_find: str, to_replace: str) -> None:
        self.map = [[to_replace if element == to_find else element for element in row] for row in self.map]

    def change_current_symbol(self, new_symbol: str) -> None:
        if new_symbol == Map.START_SYMBOL or new_symbol == Map.END_SYMBOL or new_symbol == Map.PATH_SYMBOL:
            self.current_symbol = new_symbol

    def get_map_indexes(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        row = coord[1] // self.tile_size
        column = coord[0] // self.tile_size
        return row, column

    def ready(self):
        found_start = False
        found_end = False
        for row in self.map:
            if found_end and found_start:
                break
            if Map.END_SYMBOL in row:
                found_end = True
            if Map.START_SYMBOL in row:
                found_start = True

        return found_end and found_start

    def resize_map(self, new_tile_size: int) -> None:
        self.tile_size = new_tile_size
        self.end_pos = (
            self.org_start[0] + ((self.org_end[0] - self.org_start[0]) // self.tile_size + 1) * self.tile_size,
            self.org_start[1] + ((self.org_end[1] - self.org_start[1]) // self.tile_size + 1) * self.tile_size
        )
        delta_width = (self.end_pos[0] - self.org_end[0]) // 2
        self.start_pos = self.org_start[0] - delta_width, self.org_start[1]
        self.end_pos = self.end_pos[0] - delta_width, self.end_pos[1]
        self.num_of_rows = (self.end_pos[1] - self.start_pos[1]) // self.tile_size
        self.num_of_cols = (self.end_pos[0] - self.start_pos[0]) // self.tile_size

        new_map = [[Map.PATH_SYMBOL for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

        for y, row in enumerate(new_map):
            for x, column in enumerate(row):
                if y < len(self.map) and x < len(self.map[0]):
                    new_map[y][x] = self.map[y][x]

        self.map = new_map

    def reset_grid(self) -> None:
        self.map = [[Map.PATH_SYMBOL for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

    def visit_place_on_map(self, coord: Tuple[int, int], sc: Surface) -> None:
        # self.map[coord[0]][coord[1]] = Map.VISITED_SYMBOL
        x = coord[1] * self.tile_size + self.start_pos[0]
        y = coord[0] * self.tile_size + self.start_pos[1]
        draw.rect(sc, (61, 90, 254), (x, y, self.tile_size, self.tile_size))
        pygame.display.flip()

    def show_solution(self, path: List[Tuple[int, int]], sc: Surface) -> None:
        for coord in path:
            # self.map[coord[0]][coord[1]] = Map.SOLUTION_SYMBOL
            x = coord[1] * self.tile_size + self.start_pos[0]
            y = coord[0] * self.tile_size + self.start_pos[1]
            draw.rect(sc, (144, 202, 249), (x, y, self.tile_size, self.tile_size))
            pygame.display.flip()

    # def restart_map(self):
    #     self.map = [[Map.WALL_SYMBOL for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

    def generate_maze(self) -> None:
        # Directions (up, down, left, right)
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        def is_valid_move(x, y):
            if x < 0 or x >= self.num_of_rows or y < 0 or y >= self.num_of_cols:
                return False
            if self.map[x][y] != Map.WALL_SYMBOL:
                return False
            return True

        def carve_path(x, y):
            self.map[x][y] = Map.PATH_SYMBOL
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid_move(nx, ny):
                    mid_x, mid_y = x + dx // 2, y + dy // 2
                    self.map[mid_x][mid_y] = Map.PATH_SYMBOL
                    carve_path(nx, ny)

        self.map = [[Map.WALL_SYMBOL for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

        # Starting point
        start_x, start_y = 0, 0
        carve_path(start_x, start_y)

        # Set the start and end symbols
        while not self.ready():
            start_y = random.randint(0, self.num_of_rows - 1)
            start_x = random.randint(0, self.num_of_cols - 1)
            end_y = random.randint(0, self.num_of_rows - 1)
            end_x = random.randint(0, self.num_of_cols - 1)

            if self.map[start_y][start_x] == Map.PATH_SYMBOL and self.map[end_y][end_x] == Map.PATH_SYMBOL:
                self.map[start_y][start_x] = Map.START_SYMBOL
                self.map[end_y][end_x] = Map.END_SYMBOL
