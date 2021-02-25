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

        def get_room_at(x, y):
            return next([i for i in potential_rooms if i.x_coord == x and i.y_coord == y])

        for x in 0..width:
            for y in 0..height:
                potential_rooms.append(Room(x, y))
        for x in 0..width:
            for y in 0..height:
                room = get_room_at(x, y)
                if x == 0:
                    room.possible_neighbors.append(get_room_at(x+1, y))
                elif x == self.width-1:
                    room.possible_neighbors.append(get_room_at(x-1, y))
                else:
                    room.possible_neighbors.append(get_room_at(x + 1, y))
                    room.possible_neighbors.append(get_room_at(x - 1, y))
                if y == 0:
                    room.possible_neighbors.append(get_room_at(x, y + 1))
                elif y == self.height-1:
                    room.possible_neighbors.append(get_room_at(x, y-1))
                else:
                    room.possible_neighbors.append(get_room_at(x, y + 1))
                    room.possible_neighbors.append(get_room_at(x, y - 1))
        # at this point, all rooms are created and linked to each other
        # override start room and end room to disconnect them from anything other than the one above and below them
        start_room = get_room_at(self.entry_coords[0], self.entry_coords[1])
        start_room.possible_neighbors = [get_room_at(self.entry_coords[0], self.entry_coords[1]-1)]

        end_room = get_room_at(self.exit_coords[0], self.exit_coords[1])
        end_room.possible_neighbors = [get_room_at(self.exit_coords[0], self.exit_coords[1] + 1)]

        # remove stat room as an option from the rooms to the left and right
        # remove end room as an option from the rooms to the left and right

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

        for i in 0..remaining_doors:
            pass
            # add more missing connections

        self.rooms = potential_rooms

    def __str__(self):
        return "something"


class RoomCollection:
    def __init__(self, rooms):
        self.rooms = rooms

    def get_all_neighbors(self):
        neighbors = []
        for room in self.rooms:
            neighbors.append([x for x in room.possible_neighbors if x not in neighbors])
        return neighbors

    def get_room_by_coords(self, x, y):
        return next([i for i in self.rooms if i.x_coord == x and i.y_coord == y])

    def get_row(self, y):
        return [i for i in self.rooms if i.y_coord == y]

    def get_col(self, x):
        return [i for i in self.rooms if i.x_coord == x]


class Room:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.possible_neighbors = []
        self.connected_neighbors = []

    def is_starting_room(self, map):
        return self.x_coord == map.entry_coords[0] and self.y_coord == map.entry_coords[1]

    def is_exit_room(self, map):
        return self.x_coord == map.exit_coords[0] and self.y_coord == map.exit_coords[1]

