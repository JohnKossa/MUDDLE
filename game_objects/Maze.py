import random

from .Room import Room, RoomUtils


class Maze:
    def __init__(self, width=None, height=None, entry_coords=None, exit_coords=None):
        if width is None or height is None:
            print("Cannot instantiate a maze without a width and height")
        else:
            self.width = width
            self.height = height
            self.entry_coords = entry_coords
            self.exit_coords = exit_coords
            self.rooms = []

    def generate_maze(self, difficulty=2):
        potential_rooms = []

        for x in range(self.width):
            for y in range(self.height):
                potential_rooms.append(Room(x, y))
        for x in range(self.width):
            for y in range(self.height):
                room = RoomUtils.get_room_by_coords(x, y, potential_rooms)
                if x == 0:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x + 1, y, potential_rooms))
                elif x == self.width-1:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x - 1, y, potential_rooms))
                else:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x + 1, y, potential_rooms))
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x - 1, y, potential_rooms))
                if y == 0:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x, y + 1, potential_rooms))
                elif y == self.height-1:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x, y - 1, potential_rooms))
                else:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x, y + 1, potential_rooms))
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x, y - 1, potential_rooms))

        start_x = self.entry_coords[0]
        start_y = self.entry_coords[1]
        start_room = RoomUtils.get_room_by_coords(start_x, start_y, potential_rooms)
        start_room.possible_neighbors = [RoomUtils.get_room_by_coords(start_x, start_y-1, potential_rooms)]
        RoomUtils.get_room_by_coords(start_x - 1, start_y, potential_rooms).possible_neighbors.remove(start_room)
        RoomUtils.get_room_by_coords(start_x + 1, start_y, potential_rooms).possible_neighbors.remove(start_room)

        exit_x = self.exit_coords[0]
        exit_y = self.exit_coords[1]
        end_room = RoomUtils.get_room_by_coords(exit_x, exit_y, potential_rooms)
        end_room.possible_neighbors = [RoomUtils.get_room_by_coords(exit_x, exit_y+1, potential_rooms)]
        RoomUtils.get_room_by_coords(exit_x-1, exit_y, potential_rooms).possible_neighbors.remove(end_room)
        RoomUtils.get_room_by_coords(exit_x+1, exit_y, potential_rooms).possible_neighbors.remove(end_room)

        max_doors = 4 * (self.width - 1) * (self.height - 1) + 3 * (self.height - 2) * 2 + 3 * (
                    self.width - 2) * 2 + 4 * 2 - 4
        min_doors = self.width * self.height

        path = [start_room]
        while len(path) < min_doors:
            possible_neighbors = RoomUtils.get_all_neighbors(path)
            to_add = random.choice(possible_neighbors)
            if to_add is None:
                print("no more rooms to add")
                break
            # TODO Door order is picked to increase "maziness", possibly refactor to make truely random
            if RoomUtils.get_neighbor_in_in_direction(to_add, "north", path) is not None:
                path_room = RoomUtils.get_neighbor_in_in_direction(to_add, "north", path)
                to_add.north_door = path_room
                path_room.south_door = to_add
                to_add.possible_neighbors.remove(path_room)
                path_room.possible_neighbors.remove(to_add)
                path.append(to_add)
            elif RoomUtils.get_neighbor_in_in_direction(to_add, "east", path) is not None:
                path_room = RoomUtils.get_neighbor_in_in_direction(to_add, "east", path)
                to_add.east_door = path_room
                path_room.west_door = to_add
                to_add.possible_neighbors.remove(path_room)
                path_room.possible_neighbors.remove(to_add)
                path.append(to_add)
            elif RoomUtils.get_neighbor_in_in_direction(to_add, "west", path) is not None:
                path_room = RoomUtils.get_neighbor_in_in_direction(to_add, "west", path)
                to_add.west_door = path_room
                path_room.east_door = to_add
                to_add.possible_neighbors.remove(path_room)
                path_room.possible_neighbors.remove(to_add)
                path.append(to_add)
            elif RoomUtils.get_neighbor_in_in_direction(to_add, "south", path) is not None:
                path_room = RoomUtils.get_neighbor_in_in_direction(to_add, "south", path)
                to_add.south_door = path_room
                path_room.north_door = to_add
                to_add.possible_neighbors.remove(path_room)
                path_room.possible_neighbors.remove(to_add)
                path.append(to_add)
            else:
                self.rooms = potential_rooms
                print(self)
                print("Tile in question: {},{}".format(to_add.x_coord, to_add.y_coord))
                raise Exception("Selected room has no connection to path. Something bad has happened. {}".format(to_add))

        remaining_doors = (max_doors - min_doors) // difficulty

        for i in range(remaining_doors):
            pass
            # add more missing connections

        self.rooms = potential_rooms

    def __str__(self):
        result = ""
        grid = [['X' for i in range(self.width*2 + 1)] for ii in range(self.height*2+1)]
        count = 0
        for room in self.rooms:
            y_coord = 2*room.y_coord+1
            x_coord = 2*room.x_coord+1
            count += 1
            if room.x_coord == self.entry_coords[0] and room.y_coord == self.entry_coords[1]:
                grid[y_coord][x_coord] = "S"
            elif room.x_coord == self.exit_coords[0] and room.y_coord == self.exit_coords[1]:
                grid[y_coord][x_coord] = "E"
            else:
                grid[y_coord][x_coord] = "O"
            if room.north_door is not None:
                grid[y_coord-1][x_coord] = "-"
            if room.south_door is not None:
                grid[y_coord+1][x_coord] = "-"
            if room.west_door is not None:
                grid[y_coord][x_coord-1] = "|"
            if room.east_door is not None:
                grid[y_coord][x_coord+1] = "|"
        for row in grid:
            result += "".join(row)+"\n"
        return result
