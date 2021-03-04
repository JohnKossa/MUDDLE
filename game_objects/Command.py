from discord_objects.DiscordUser import DiscordUser, UserUtils
from game_objects.Player import Player


class Command:
    def __init__(self):
        self.parameters = []


class Exit(Command):
    @staticmethod
    def do_action(game, params, message):
        target_user = UserUtils.get_character_by_username(message.author, game.discord_users)
        if target_user is None or target_user.current_character is None:
            return "You don't currently have a character. Use the !NewCharacter command to create one."
        target_player = target_user.current_character
        room = target_player.current_room
        direction = params[0]
        door = room.get_door(direction)
        if door is None:
            return "Invalid direction. Room has no {} exit.".format(direction)
        target_player.current_room = door
        return str(target_player.current_room)


class RebuildMaze(Command):
    @staticmethod
    def do_action(game, params, message):
        width = int(params[0])
        height = int(params[1])
        difficulty = int(params[2])
        game.init_maze(width, height, difficulty)
        return "Maze rebuilt!\n"+str(game.maze)


class NewCharacter(Command):
    @staticmethod
    def do_action(game, params, message):
        new_discord_user = DiscordUser()
        new_player = Player()
        new_discord_user.username = message.author
        new_discord_user.current_character = new_player
        game.register_player(new_player)
        game.discord_users.append(new_discord_user)
        new_player.discord_user = new_discord_user
        return "New character created for {}".format(message.author)
