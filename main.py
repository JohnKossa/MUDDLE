from game_objects.Maze import Maze

maze = Maze(width=10, height=10, entry_coords=(5, 9), exit_coords=(5, 0))
maze.generate_maze()
print(maze)
