import random

from game_objects.MazeRoom  import MazeRoom, RoomUtils


class Maze:
    def __init__(self, width=None, height=None):
        if width is None or height is None:
            raise Exception("Cannot instantiate a maze without a width and height")
        else:
            self.width = width
            self.height = height
            self.rooms = []
            self.entry_room = None
            self.exit_room = None

    @property
    def last_row_index(self):
        return self.height-1

    @property
    def last_col_index(self):
        return self.width-1

    def generate_maze(self, entry_coords, exit_coords, difficulty=2):
        potential_rooms = []

        opposite_directions = {
            "north": "south",
            "south": "north",
            "west": "east",
            "east": "west"
        }

        for x in range(self.width):
            for y in range(self.height):
                potential_rooms.append(MazeRoom(x, y))
        for x in range(self.width):
            for y in range(self.height):
                room = RoomUtils.get_room_by_coords(x, y, potential_rooms)
                if x == 0:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x + 1, y, potential_rooms))
                elif x == self.last_col_index:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x - 1, y, potential_rooms))
                else:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x + 1, y, potential_rooms))
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x - 1, y, potential_rooms))
                if y == 0:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x, y + 1, potential_rooms))
                elif y == self.last_row_index:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x, y - 1, potential_rooms))
                else:
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x, y + 1, potential_rooms))
                    room.possible_neighbors.append(RoomUtils.get_room_by_coords(x, y - 1, potential_rooms))

        start_x = entry_coords[0]
        start_y = entry_coords[1]
        start_room = RoomUtils.get_room_by_coords(start_x, start_y, potential_rooms)
        start_room.possible_neighbors = [RoomUtils.get_room_by_coords(start_x, start_y-1, potential_rooms)]
        RoomUtils.get_room_by_coords(start_x - 1, start_y, potential_rooms).possible_neighbors.remove(start_room)
        RoomUtils.get_room_by_coords(start_x + 1, start_y, potential_rooms).possible_neighbors.remove(start_room)

        exit_x = exit_coords[0]
        exit_y = exit_coords[1]
        end_room = RoomUtils.get_room_by_coords(exit_x, exit_y, potential_rooms)
        end_room.possible_neighbors = [RoomUtils.get_room_by_coords(exit_x, exit_y+1, potential_rooms)]
        RoomUtils.get_room_by_coords(exit_x-1, exit_y, potential_rooms).possible_neighbors.remove(end_room)
        RoomUtils.get_room_by_coords(exit_x+1, exit_y, potential_rooms).possible_neighbors.remove(end_room)

        path = [start_room]
        while len(path) < (self.width * self.height):
            possible_neighbors = RoomUtils.get_all_neighbors(path)
            to_add = random.choice(possible_neighbors)
            if to_add is None:
                raise Exception("No more rooms to add. If this state is reached, it may indicate an error.")

            def connect_to_direction(direction):
                path_room = RoomUtils.get_neighbor_in_in_direction(to_add, direction, path)
                to_add.set_door(direction, path_room)
                path_room.set_door(opposite_directions[direction], to_add)
                to_add.possible_neighbors.remove(path_room)
                path_room.possible_neighbors.remove(to_add)

            directions = ["north", "south", "east", "west"]
            random.shuffle(directions)
            valid_directions = filter(lambda direction: RoomUtils.get_neighbor_in_in_direction(to_add, direction, path) is not None, directions)
            connect_to_direction(next(valid_directions))
            path.append(to_add)

        # remaining possible doors = sum up all possible_neighbors from all doors and divide by 2
        remaining_doors = sum([len(x.possible_neighbors) for x in potential_rooms]) // 2 // difficulty

        for i in range(remaining_doors):
            # randomly select a new connection to add to the maze
            available_rooms = [*filter(lambda room: len(room.possible_neighbors) > 0, potential_rooms)]
            if len(available_rooms) == 0:
                raise Exception("Ran out of rooms when trying to adjust for difficulty.")
            to_add = random.choice(available_rooms)
            directions = ["north", "south", "east", "west"]
            random.shuffle(directions)
            valid_directions = filter(
                lambda direction: RoomUtils.get_neighbor_in_in_direction(to_add, direction, path) is not None,
                directions)
            connect_to_direction(next(valid_directions))

        self.rooms = potential_rooms
        self.entry_room = RoomUtils.get_room_by_coords(entry_coords[0], entry_coords[1], self.rooms)
        self.exit_room = RoomUtils.get_room_by_coords(exit_coords[0], exit_coords[1], self.rooms)

    def __str__(self):
        result = ""
        grid = [['X' for i in range(self.width*2 + 1)] for ii in range(self.height*2+1)]
        count = 0
        for room in self.rooms:
            y_coord = 2*room.y_coord+1
            x_coord = 2*room.x_coord+1
            count += 1
            if room == self.entry_room:
                grid[y_coord][x_coord] = "S"
            elif room == self.exit_room:
                grid[y_coord][x_coord] = "E"
            else:
                grid[y_coord][x_coord] = " "
            if room.north_door is not None:
                grid[y_coord-1][x_coord] = "-"
            if room.south_door is not None:
                grid[y_coord+1][x_coord] = "-"
            if room.west_door is not None:
                grid[y_coord][x_coord-1] = "|"
            if room.east_door is not None:
                grid[y_coord][x_coord+1] = "|"
        for row in grid:
            result += " ".join(row)+"\n"
        return "```"+result+"```"
