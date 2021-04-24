from __future__ import annotations
from typing import List, Optional

from game_objects.Commands.Command import Command
from game_objects.Commands.PartialCombatCommands.ExitCommand import Exit
from game_objects.Commands.NoncombatCommands.ExitMazeCommand import ExitMaze
from game_objects.Room import Room
from utils.TextHelpers import enumerate_objects


class MazeRoom(Room):
    def __init__(self, x_coord: int, y_coord: int):
        super(MazeRoom, self).__init__(name=f"{x_coord},{y_coord}")
        self.x_coord: int = x_coord
        self.y_coord: int = y_coord
        self.width: int = 1
        self.height: int = 1
        self.possible_neighbors: List[MazeRoom] = []
        self.north_door: Optional[MazeRoom] = None
        self.east_door: Optional[MazeRoom] = None
        self.south_door: Optional[MazeRoom] = None
        self.west_door: Optional[MazeRoom] = None
        self.description_template = None
        self.starting_room = False
        self.exit_room = False

    @property
    def connected_neighbors(self) -> List[Room]:
        result = []
        if self.north_door is not None:
            result.append(self.north_door)
        if self.east_door is not None:
            result.append(self.east_door)
        if self.south_door is not None:
            result.append(self.south_door)
        if self.west_door is not None:
            result.append(self.west_door)
        return result

    @property
    def num_neighbors(self) -> int:
        count = 0
        if self.north_door is not None:
            count = count+1
        if self.east_door is not None:
            count = count+1
        if self.south_door is not None:
            count = count+1
        if self.west_door is not None:
            count = count+1
        return count

    def get_door(self, direction: str) -> MazeRoom:
        doors = {
            "north": self.north_door,
            "east": self.east_door,
            "south": self.south_door,
            "west": self.west_door,
            "n": self.north_door,
            "e": self.east_door,
            "s": self.south_door,
            "w": self.west_door
        }
        if direction.lower() in doors.keys():
            return doors[direction.lower()]

    def set_door(self, direction: str, val: Room) -> None:
        if direction == "north":
            self.north_door = val
        elif direction == "east":
            self.east_door = val
        elif direction == "south":
            self.south_door = val
        elif direction == "west":
            self.west_door = val

    def describe_exits(self) -> str:
        exits = {
            "North": self.north_door,
            "East": self.east_door,
            "South": self.south_door,
            "West": self.west_door
        }
        valid_exits = [*filter(lambda x: exits[x] is not None, exits.keys())]
        exit_count = len(valid_exits)
        if exit_count == 1:
            return f"There is one exit to the {valid_exits[0]}"
        elif exit_count == 2:
            return f"Exits are to the {valid_exits[0]} and {valid_exits[1]}"
        elif exit_count > 2:
            formatted_list = enumerate_objects(valid_exits)
            return f"Exits include {formatted_list}"

    def get_commands(self) -> List[Command]:
        to_return = super().get_commands()
        if self.starting_room or self.exit_room:
            to_return = to_return + [ExitMaze()]
        return to_return


class RoomUtils:
    @staticmethod
    def get_all_neighbors(rooms: List[MazeRoom]) -> List[MazeRoom]:
        neighbors = []
        for room in rooms:
            if room is not None:
                neighbors = neighbors + [x for x in room.possible_neighbors if x not in neighbors and x not in rooms]
            else:
                raise Exception("null room in passed rooms")
        return neighbors

    @staticmethod
    def get_room_by_coords(x: int, y: int, rooms: List[Room]) -> Optional[MazeRoom]:
        return next(iter(filter(lambda i: i.x_coord == x and i.y_coord == y, rooms)), None)

    @staticmethod
    def get_neighbor_in_in_direction(room: MazeRoom, direction: str, rooms: List[MazeRoom]) -> Optional[MazeRoom]:
        if room is None:
            return None
        offsets = {
            "north": (0, -1),
            "east": (1, 0),
            "south": (0, 1),
            "west": (-1, 0)
        }
        result = RoomUtils.get_room_by_coords(room.x_coord+offsets[direction][0], room.y_coord+offsets[direction][1], rooms)
        if result in room.possible_neighbors:
            return result
        return None

    @staticmethod
    def get_row(y: int, rooms: List[MazeRoom]) -> List[MazeRoom]:
        return [i for i in rooms if i.y_coord == y]

    @staticmethod
    def get_col(x: int, rooms: List[MazeRoom]) -> List[MazeRoom]:
        return [i for i in rooms if i.x_coord == x]
