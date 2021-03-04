import os
import re

import discord
from dotenv import load_dotenv
from game_objects.Command import Exit, RebuildMaze, NewCharacter

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


class CustomClient(discord.Client):
    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        user = self.user
        author = message.author
        content = message.content
        channel = message.channel

        if not content.startswith("!"):
            return

        matches = re.match(r"^!(\w+)((?:\s\w+)+)?$", message.content)
        command = matches.group(1)
        param_match = matches.group(2)
        params = []
        if param_match:
            params = [m.group(0) for m in re.finditer(r'\w+', param_match)]

        commands = {
            "sayhello": lambda: "Hello World!",
            "showmap": lambda: str(game.maze),
            "exit": lambda: Exit.do_action(game, params, message),
            "rebuildmaze": lambda: RebuildMaze.do_action(game, params, message),
            "newcharacter": lambda: NewCharacter.do_action(game, params, message)
        }

        if command.lower() in commands.keys():
            await channel.send(commands[command.lower()]())

        if command.lower() == "get" and params[0].lower() == "ye" and params[1].lower() == "flask":
            await channel.send("You can't get ye flask")

    async def on_error(self, event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise


client = CustomClient()
game = None


def run(game_ref):
    global game
    game = game_ref
    client.run(TOKEN)
