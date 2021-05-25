from __future__ import annotations
from typing import List, Optional

from game_objects.Commands.Command import Command
from game_objects.Maze.MazeRoom import MazeRoom


class SafeRoom(MazeRoom):
    descriptions = None

    def __init__(self, x_coord: int, y_coord: int):
        super(SafeRoom, self).__init__(x_coord, y_coord)

    def describe_room(self) -> str:
        if SafeRoom.descriptions is None:
            import json
            with open(f"templates/rooms/saferoom.json", "r") as infile:
                MazeRoom.descriptions = json.load(infile)
        import random
        random.seed(self.description_seed)
        selected_description = random.choices(MazeRoom.descriptions, weights=list(
            description.get("weight", 1) for description in MazeRoom.descriptions))[0]["description_long"]
        if isinstance(selected_description, list):
            return "\n".join(selected_description)
        if isinstance(selected_description, str):
            return selected_description
        return ""

    @staticmethod
    def clone_from_MazeRoom(maze_room: MazeRoom):
        to_return = SafeRoom(maze_room.x_coord, maze_room.y_coord)
        to_return.width = maze_room.width
        to_return.height = maze_room.height
        to_return.north_door = maze_room.north_door
        to_return.east_door = maze_room.east_door
        to_return.south_door = maze_room.south_door
        to_return.west_door = maze_room.west_door
        if to_return.north_door is not None:
            to_return.north_door.south_door = to_return
        if to_return.south_door is not None:
            to_return.south_door.north_door = to_return
        if to_return.east_door is not None:
            to_return.east_door.west_door = to_return
        if to_return.west_door is not None:
            to_return.west_door.east_door = to_return
        maze_room.north_door = None
        maze_room.south_door = None
        maze_room.east_door = None
        maze_room.west_door = None
        return to_return

    def get_commands(self, game) -> List[Command]:
        to_return = super().get_commands(game)
        return to_return
