import discord
import os
import re

from dotenv import load_dotenv

from discord_objects.DiscordUser import DiscordUser, UserUtils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True


class CustomClient(discord.Client):
    def __init__(self, intents=None):
        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        print('Collecting users')
        guild = self.guilds[0]
        async for member in guild.fetch_members():
            if UserUtils.get_user_by_username(str(member), game.discord_users) is None:
                game.discord_users.append(DiscordUser(username=str(member)))
        print('Users collected. Added {} users.'.format(len(game.discord_users)))
        UserUtils.print_all(game.discord_users)

    async def on_message(self, message):
        user = self.user
        author = message.author
        content = message.content
        channel = message.channel

        if author == user:  # ignore own messages
            return

        # Collect user if not in users

        discord_user = UserUtils.get_user_by_username(str(author), game.discord_users)
        if discord_user is None:
            print("New user found. Adding...")
            discord_user = DiscordUser(username=str(author))
            game.discord_user.append(discord_user)
        else:
            print("Existing user found")

        if not content.startswith("!"):
            return

        command_list = discord_user.get_commands()

        matches = re.match(r"^!(\w+)((?:\s\w+)+)?$", message.content)
        command = matches.group(1)
        param_match = matches.group(2)
        params = []
        if param_match:
            params = [m.group(0) for m in re.finditer(r'\w+', param_match)]

        matched_command = None
        for possible_command in command_list:
            lower_aliases = [x.lower() for x in possible_command.aliases]
            if command.lower() in lower_aliases:
                print("Matched input {} to {}".format(command, possible_command.command_name()))
                matched_command = possible_command

        if matched_command is not None:
            await channel.send(matched_command.do_action(game, params, message))
            return

        if command.lower() == "get" and params[0].lower() == "ye" and params[1].lower() == "flask":
            await channel.send("You can't get ye flask")

    async def on_error(self, event, *args, **kwargs):
        with open('err.log', 'a') as f:
            if event == 'on_message':
                f.write(f'Unhandled message: {args[0]}\n')
            else:
                raise


client = CustomClient(intents=intents)
game = None


def run(game_ref):
    global game
    game = game_ref
    client.run(TOKEN)
