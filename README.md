# Maze Pathfinder Visualizer
#### Video Demo: [VIDEO](https://www.youtube.com/watch?v=GoKL_9Ekfzc)
#### Description:
Maze Pathfinder Visualizer is a Python desktop application developed using the Pygame library. It allows users to draw mazes and visualize various pathfinding algorithms as they solve the maze. Users can customize the size of the maze and the speed at which the algorithm operates. This project aims to help users understand the behavior and efficiency of different pathfinding algorithms through visual demonstration.

## Features
- **Maze Drawing**: Users can manually draw mazes.
- **Algorithm Selection**: Choose from multiple pathfinding algorithms (e.g., A*, Dijkstra, BFS, DFS, Random Walk).
- **Visualization**: Watch the algorithm solve the maze in real-time.
- **Settings**: Adjust the maze size and the visualization speed.

## Files
- **main.py**: The main script that runs the application.
- **game_state.py**: Manages the state of the game, including the current maze and the algorithm being visualized.
- **key_handler_class.py**: Handles key inputs from the user.
- **map_class.py**: Manages the creation and representation of the maze.
- **utils.py**: Contains utility functions used throughout the project.
- **algorithms/**
  - **algorithm_manager.py**: Manages the different pathfinding algorithms and their execution.
  - **astar_shortest_path.py**: Implements the A* shortest path algorithm.
  - **breadth_first_search.py**: Implements the breadth-first search algorithm.
  - **depth_first_search.py**: Implements the depth-first search algorithm.
  - **dijkstra_algorithm.py**: Implements Dijkstra's algorithm.
  - **random_walk.py**: Implements a random walk algorithm.
- **user_interface/**
  - **button_class.py**: Manages button UI components.
  - **button_group.py**: Manages groups of buttons.
  - **slider_class.py**: Manages slider UI components.

## Design Choices
- **Modularity**: Each algorithm is implemented in a separate module, allowing easy addition of new algorithms.
- **User Interface**: The interface is designed to be intuitive, with clear controls for drawing mazes and starting visualizations.
- **Performance**: The application is optimized to handle large mazes and high-speed visualizations without significant lag.

## Setup

## Usage
1. Run the application using `python main.py`.
2. Draw a maze using the mouse.
3. Select a pathfinding algorithm from the menu.
4. Adjust settings if necessary.
5. Click "Start" to visualize the algorithm solving the maze.

## Future Enhancements
- Adding more algorithms.
- Improving the user interface with more controls and options.
- Improving the visualization.
- Allowing users to save and load mazes.

This project was created as part of the CS50x course final project.

## Acknowledgements
- CS50x for the foundational knowledge.
- Pygame library for making game development in Python straightforward.

## To Do

- [x] Implement interface Slider to create sliders for changing values in the app
- [x] Implement interface Buttons Class to create buttons in the app
- [x] Implement more algorithms
- [x] Implement Algorithm manager
- [ ] Implement buttons for editing and starting
- [ ] Implement feature to generate a random maze
- [ ] Implement menu
