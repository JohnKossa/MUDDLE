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
        door = room.get_door(direction)
        if door is None:
            return "Invalid direction. Room has no {} exit.".format(direction)
        target_player.current_room = door
        return str(target_player.current_room)


class Parameter:
    def __init__(self):
        pass
