class DepthFirstSearch:
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
        stack = [(self.start_position, [self.start_position])]

        while stack:
            current_pos, path = stack.pop()
            row, col = current_pos
            self.visited.add(current_pos)

            # Yield the current step for visualization or other purposes
            yield current_pos

            if current_pos == self.end_position:
                self.solution = path
                return

            neighbors = self.find_neighbors(row, col)
            for neighbor in neighbors:
                if neighbor not in self.visited and self.map_maze[neighbor[0]][neighbor[1]] != self.wall_symbol:
                    stack.append((neighbor, path + [neighbor]))
                    self.visited.add(neighbor)

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
