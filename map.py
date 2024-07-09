from typing import Tuple
from pygame import Surface, draw, mouse


class Map:
    def __init__(self, tile_size: int, start_pos: Tuple[int, int], end_pos: Tuple[int, int]):
        self.tile_size = tile_size
        self.org_start = start_pos
        self.org_end = end_pos
        self.end_pos = (self.org_start[0] + ((self.org_end[0] - self.org_start[0]) // self.tile_size + 1) * self.tile_size,
                        self.org_start[1] + ((self.org_end[1] - self.org_start[1]) // self.tile_size + 1) * self.tile_size)
        #########
        delta_width = (self.end_pos[0] - self.org_end[0]) // 2
        self.start_pos = self.org_start[0] - delta_width, self.org_start[1]
        self.end_pos = self.end_pos[0] - delta_width, self.end_pos[1]
        #########
        self.num_of_rows = (self.end_pos[1] - self.start_pos[1]) // self.tile_size
        self.num_of_cols = (self.end_pos[0] - self.start_pos[0]) // self.tile_size
        self.map = [["x" for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

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

    def draw_map(self, sc: Surface) -> None:
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
                if col == "#":  # Path
                    draw.rect(sc, (160, 100, 80), (x, y, self.tile_size, self.tile_size))
                if col == "x":  # Wall
                    draw.rect(sc, (110, 110, 110), (x + 1, y + 1, self.tile_size - 2, self.tile_size - 2))

    def update_map(self) -> None:
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
            if self.map[row][column] == "x":
                self.map[row][column] = "#"

        elif mouse_buttons[2]:
            self.map[row][column] = "x"

    def get_map_indexes(self, coord: Tuple[int, int]) -> Tuple[int, int]:
        row = coord[1] // self.tile_size
        column = coord[0] // self.tile_size
        return row, column

    def resize_map(self, new_tile_size) -> None:
        self.tile_size = new_tile_size
        self.end_pos = (self.org_start[0] + ((self.org_end[0] - self.org_start[0]) // self.tile_size + 1) * self.tile_size,
                        self.org_start[1] + ((self.org_end[1] - self.org_start[1]) // self.tile_size + 1) * self.tile_size)
        delta_width = (self.end_pos[0] - self.org_end[0]) // 2
        self.start_pos = self.org_start[0] - delta_width, self.org_start[1]
        self.end_pos = self.end_pos[0] - delta_width, self.end_pos[1]
        self.num_of_rows = (self.end_pos[1] - self.start_pos[1]) // self.tile_size
        self.num_of_cols = (self.end_pos[0] - self.start_pos[0]) // self.tile_size

        new_map = [["x" for _ in range(self.num_of_cols)] for _ in range(self.num_of_rows)]

        for y, row in enumerate(new_map):
            for x, column in enumerate(row):
                if y < len(self.map) and x < len(self.map[0]):
                    new_map[y][x] = self.map[y][x]

        self.map = new_map
