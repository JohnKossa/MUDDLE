from game_objects.maze import Maze

maze = Maze(width=10, height=10, entry_coords=(5, 0), exit_coords=(5, 9))
maze.generate_maze()
print(maze)
