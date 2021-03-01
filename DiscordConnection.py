import os
import re

import discord
from dotenv import load_dotenv

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
        commands = {
            "SayHello": lambda: channel.send("Hello World!"),
            "SayGoodbye": lambda: channel.send("Goodbye World!"),
            "ShowMap": lambda: channel.send("```"+str(game.maze)+"```")
        }
        if not content.startswith("!"):
            return

        for k, v in commands.items():
            if re.search("^!" + k, content):
                await v()

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
