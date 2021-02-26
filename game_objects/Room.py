class Room:
    def __init__(self, x_coord, y_coord):
        self.name = "{},{}".format(x_coord, y_coord)
        self.template = None
        self.fixtures = []
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.possible_neighbors = []
        self.north_door = None
        self.east_door = None
        self.south_door = None
        self.west_door = None
        self.description_template = None

    @property
    def connected_neighbors(self):
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

    def is_starting_room(self, maze):
        return self.x_coord == maze.entry_coords[0] and self.y_coord == maze.entry_coords[1]

    def is_exit_room(self, maze):
        return self.x_coord == maze.exit_coords[0] and self.y_coord == maze.exit_coords[1]


class RoomUtils:
    @staticmethod
    def get_all_neighbors(rooms):
        neighbors = []
        for room in rooms:
            if room is not None:
                neighbors = neighbors + [x for x in room.possible_neighbors if x not in neighbors and x not in rooms]
            else:
                raise Exception("null room in passed rooms")
        return neighbors

    @staticmethod
    def get_room_by_coords(x, y, rooms):
        return next(iter(filter(lambda i: i.x_coord == x and i.y_coord == y, rooms)), None)

    @staticmethod
    def get_neighbor_in_in_direction(room, direction, rooms):
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
    def get_row(y, rooms):
        return [i for i in rooms if i.y_coord == y]

    @staticmethod
    def get_col(x, rooms):
        return [i for i in rooms if i.x_coord == x]