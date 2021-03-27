from game_objects.Commands.Command import Command


class NoncombatCommand(Command):
    # Commands that can only be used out of combat
    def __init__(self):
        super().__init__()
