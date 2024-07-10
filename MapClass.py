from typing import Tuple, List
from pygame import Surface, draw, mouse


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
        self.map = [[Map.WALL_SYMBOL for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]
        self.map[0][0] = Map.START_SYMBOL
        self.map[0][5] = Map.END_SYMBOL

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
            if self.map[row][column] == Map.WALL_SYMBOL:
                self.map[row][column] = Map.PATH_SYMBOL

        elif mouse_buttons[2]:
            self.map[row][column] = Map.WALL_SYMBOL

    def get_map_indexes(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        row = coord[1] // self.tile_size
        column = coord[0] // self.tile_size
        return row, column

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

        new_map = [[Map.WALL_SYMBOL for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

        for y, row in enumerate(new_map):
            for x, column in enumerate(row):
                if y < len(self.map) and x < len(self.map[0]):
                    new_map[y][x] = self.map[y][x]

        self.map = new_map

    def visit_place_on_map(self, coord: Tuple[int, int]) -> None:
        self.map[coord[0]][coord[1]] = Map.VISITED_SYMBOL

    def show_solution(self, path: List[Tuple[int, int]]) -> None:
        for coord in path:
            self.map[coord[0]][coord[1]] = Map.SOLUTION_SYMBOL

    def restart_map(self):
        self.map = [[Map.WALL_SYMBOL for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]
