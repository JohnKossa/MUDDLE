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

        start_room = RoomUtils.get_room_by_coords(self.entry_coords[0], self.entry_coords[1], potential_rooms)
        start_room.possible_neighbors = [RoomUtils.get_room_by_coords(self.entry_coords[0], self.entry_coords[1]-1, potential_rooms)]

        end_room = RoomUtils.get_room_by_coords(self.exit_coords[0], self.exit_coords[1], potential_rooms)
        end_room.possible_neighbors = [RoomUtils.get_room_by_coords(self.exit_coords[0], self.exit_coords[1]+1, potential_rooms)]

        max_doors = 4 * (self.width - 1) * (self.height - 1) + 3 * (self.height - 2) * 2 + 3 * (
                    self.width - 2) * 2 + 4 * 2 - 4
        min_doors = self.width * self.height

        # randomly add doors to the path from the set of possible connections
        # generate random door values for each possible neighbor for each room
        # add starting room to path
        # while path has less than width*height nodes
        #   get a list of all possible neighbors of all nodes in the path
        #   randomly select one of the neighbors to add
        #   add a connected neighbor ref to the room in the path
        #   add a connected neighbor ref to the room we connected to
        #   remove possible neighbor ref from path room
        #   remove possible neighbor ref from added room
        #   add the connected neighbor to the path

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
            result += "".join(row)+"\n"
        return result
