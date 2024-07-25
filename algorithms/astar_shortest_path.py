import heapq


class Astar:
    def __init__(self, map_maze, start, end, wall):
        self.map_maze = map_maze
        self.start_symbol = start
        self.end_symbol = end
        self.wall_symbol = wall
        self.start_position = self.find_position(self.start_symbol)
        self.end_position = self.find_position(self.end_symbol)
        self.visited = set()
        self.solution = list()
        self.cost = {}  # Dictionary to store the cost to reach each cell
        self.heuristic = {}  # Dictionary to store the heuristic cost

    def find_path(self):
        heap = [(0, self.start_position, [self.start_position])]
        self.cost[self.start_position] = 0
        self.heuristic[self.start_position] = self.manhattan_distance(self.start_position, self.end_position)

        while heap:
            current_f, current_pos, path = heapq.heappop(heap)
            row, col = current_pos

            # Yield the current step for visualization or other purposes
            yield current_pos

            if current_pos == self.end_position:
                self.solution = path
                return

            if current_pos in self.visited:
                continue

            self.visited.add(current_pos)

            neighbors = self.find_neighbors(row, col)
            for neighbor in neighbors:
                r, c = neighbor
                if neighbor in self.visited or self.map_maze[r][c] == self.wall_symbol:
                    continue

                new_cost = self.cost[current_pos] + 1  # Assuming each move has a cost of 1
                heuristic_cost = self.manhattan_distance(neighbor, self.end_position)
                f = new_cost + heuristic_cost

                if neighbor not in self.cost or new_cost < self.cost[neighbor]:
                    self.cost[neighbor] = new_cost
                    self.heuristic[neighbor] = heuristic_cost
                    heapq.heappush(heap, (f, neighbor, path + [neighbor]))

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

    @staticmethod
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
