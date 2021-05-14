from __future__ import annotations
from typing import List, Optional

from game_objects.Commands.Command import Command
from game_objects.Maze.MazeRoom import MazeRoom


class SafeRoom(MazeRoom):
    def __init__(self, x_coord: int, y_coord: int):
        super(SafeRoom, self).__init__(x_coord, y_coord)

    def describe_room(self) -> str:
        return " ".join([
            "As you pass through the door, a golden heraldic crest appears on the door behind you.",
            "It appears this room is protected by some sort of magical seal.",
            "A tranquil fountain sits in the center of the room, lit not by torches, but candles placed delicately about its rim.",
            "The usual dusty floor of the dungeon has turned instead to dirt, and a few tufts of grass poke up from it.",
            "A very different sight from the rest of the rooms, this room has a somewhat calming presence to it.",
            "This may be a good place to take a rest, should the need arise."
        ])

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
