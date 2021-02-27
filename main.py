from game_objects.Maze import Maze

maze = Maze(width=21, height=21, entry_coords=(10, 20), exit_coords=(10, 0))
maze.generate_maze(difficulty=3)
print(maze)
