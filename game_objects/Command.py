import re


class Command:
    def __init__(self):
        self.parameters = []


def collect_parameters(message):
    matches = re.match(r"^!(\w+)(?:\s(\w+))*$", message.content)
    groups = matches.groups()
    command = groups[0]
    params = groups[1:]
    return params


class Exit(Command):
    def __init__(self):
        super().__init__()

    def do_action(self, game, params):
        direction = params[0]
        target_player = game.players[0]
        room = target_player.current_room
        if direction.lower() == "north":
            if room.north_door is None:
                return "Invalid direction. Room has no north exit."
            else:
                target_player.current_room = room.north_door
        elif direction.lower() == "south":
            if room.south_door is None:
                return "Invalid direction. Room has no south exit."
            else:
                target_player.current_room = room.south_door
        elif direction.lower() == "east":
            if room.east_door is None:
                return "Invalid direction. Room has no east exit."
            else:
                target_player.current_room = room.east_door
        elif direction.lower() == "west":
            if room.west_door is None:
                return "Invalid direction. Room has no west exit."
            else:
                target_player.current_room = room.west_door
        else:
            return "Invalid direction {}".format(direction)
        return str(target_player.current_room)


class Parameter:
    def __init__(self):
        pass
