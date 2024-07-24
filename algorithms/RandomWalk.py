import random


class RandomWalk:
    def __init__(self, map_maze, start, end, wall):
        self.map_maze = map_maze
        self.start_symbol = start
        self.end_symbol = end
        self.wall_symbol = wall
        self.start_position = self.find_position(self.start_symbol)
        self.end_position = self.find_position(self.end_symbol)
        self.visited = set()
        self.solution = list()

    def find_path(self):
        current_pos = self.start_position
        path = [current_pos]
        self.visited.add(current_pos)

        while current_pos != self.end_position:
            neighbors = self.find_neighbors(*current_pos)
            random.shuffle(neighbors)  # Shuffle neighbors to ensure random walk

            moved = False
            for neighbor in neighbors:
                r, c = neighbor
                if neighbor not in self.visited and self.map_maze[r][c] != self.wall_symbol:
                    current_pos = neighbor
                    path.append(current_pos)
                    self.visited.add(current_pos)
                    moved = True
                    break

            # Yield the current step for visualization or other purposes
            yield current_pos

            if not moved:
                # If no move was made (dead end), backtrack
                if path:
                    path.pop()
                    if path:
                        current_pos = path[-1]
                    else:
                        current_pos = self.select_random_edge_position()
                        path = [current_pos]
                        self.visited.add(current_pos)
                else:
                    current_pos = self.select_random_edge_position()
                    path = [current_pos]
                    self.visited.add(current_pos)

        self.solution = path if current_pos == self.end_position else []

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

    def find_position(self, symbol):
        for r, row in enumerate(self.map_maze):
            for c, value in enumerate(row):
                if value == symbol:
                    return r, c
        return None

    def select_random_edge_position(self):
        rows = len(self.map_maze)
        cols = len(self.map_maze[0])
        edges = []

        # Top and bottom rows
        for c in range(cols):
            if self.map_maze[0][c] != self.wall_symbol and (0, c) not in self.visited:
                edges.append((0, c))
            if self.map_maze[rows - 1][c] != self.wall_symbol and (rows - 1, c) not in self.visited:
                edges.append((rows - 1, c))

        # Left and right columns
        for r in range(rows):
            if self.map_maze[r][0] != self.wall_symbol and (r, 0) not in self.visited:
                edges.append((r, 0))
            if self.map_maze[r][cols - 1] != self.wall_symbol and (r, cols - 1) not in self.visited:
                edges.append((r, cols - 1))

        if edges:
            return random.choice(edges)
        else:
            raise RuntimeError("No valid edge positions available to restart from.")