import pygame
import queue


CLOCK = pygame.time.Clock()


class BreadthFirstSearch:
    def __init__(self, map_maze, start, end, wall):
        self.map_maze = map_maze
        self.start_symbol = start
        self.end_symbol = end
        self.wall_symbol = wall
        self.start_position = self.find_start(self.start_symbol)
        self.end_position = self.find_end(self.end_symbol)
        self.queue = queue.Queue()
        self.queue.put((self.start_position, [self.start_position]))
        self.visited = set()
        self.solution = list()

    def find_path(self):
        while not self.queue.empty():
            current_pos, path = self.queue.get()
            row, col = current_pos
            i = path[-1]
            # r, c = i
            yield i
            # pygame.draw.rect(
            #     draws.screen,
            #     (61, 90, 254),
            #     (c * draws.TILESIZE, r * draws.TILESIZE, draws.TILESIZE, draws.TILESIZE)
            # )
            # pygame.display.update()
            if (row, col) == self.end_position:
                self.solution = path
                with self.queue.mutex:
                    self.queue.queue.clear()
                return
                # for i in path:
                #     r, c = i
                #     pygame.draw.rect(
                #         draws.screen,
                #         (144, 202, 249),
                #         (c * draws.TILESIZE, r * draws.TILESIZE, draws.TILESIZE, draws.TILESIZE)
                #     )
                #     pygame.display.update()

                # while True:
                #     pygame.init()
                #     event = pygame.event.wait()
                #     if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                #         if not pygame.key.get_pressed()[pygame.K_SPACE]:
                #             return

            neighbors = self.find_neighbors(row, col)
            for neighbor in neighbors:
                if neighbor in self.visited:
                    continue

                r, c = neighbor
                if self.map_maze[r][c] == self.wall_symbol:
                    continue

                new_path = path + [neighbor]
                self.queue.put((neighbor, new_path))
                self.visited.add(neighbor)

        if self.end_position not in self.visited:
            pass

    def find_neighbors(self, row, col):
        neighbors = []

        if row > 0:  # up
            neighbors.append((row - 1, col))
        if row + 1 < len(self.map_maze):  # down
            neighbors.append((row + 1, col))
        if col > 0:  # left
            neighbors.append((row, col - 1))
        if col + 1 < len(self.map_maze[0]):  # right
            neighbors.append((row, col + 1))

        return neighbors

    def find_end(self, end):
        for r, row in enumerate(self.map_maze):
            for c, value in enumerate(row):
                if value == end:
                    return r, c

        return None

    def find_start(self, start):
        for r, row in enumerate(self.map_maze):
            for c, value in enumerate(row):
                if value == start:
                    return r, c

        return None
