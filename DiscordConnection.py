import os
import re

import discord
from dotenv import load_dotenv
from game_objects.Command import Exit

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

        matches = re.match(r"^!(\w+)(?:\s(\w+))*$", message.content)
        command, *params = matches.groups()

        commands = {
            "sayhello": lambda: "Hello World!",
            "saygoodbye": lambda: "Goodbye World!",
            "showmap": lambda: "```"+str(game.maze)+"```",
            "exit": lambda: Exit().do_action(game, params)
        }

        if command in commands.keys():
            await channel.send(commands[command]())

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
