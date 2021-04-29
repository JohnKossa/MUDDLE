import discord
from discord import Intents
import os
import re

from dotenv import load_dotenv
from typing import List, Optional

from discord_objects.DiscordUser import DiscordUser, UserUtils
from utils.Scheduler import Scheduler

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = Intents.default()
intents.members = True


class CustomClient(discord.Client):
    def __init__(self, intents_contract: Optional[Intents] = None):
        super().__init__(intents=intents_contract, allowed_mentions=discord.AllowedMentions(users=True))
        self.game_channel = None
        self.game = None

    async def on_ready(self) -> None:
        print(f'{self.user} has connected to Discord!')
        print('Collecting users')
        guild = self.guilds[0]
        async for member in guild.fetch_members():
            if UserUtils.get_user_by_username(str(member), self.game.discord_users) is None:
                self.game.discord_users.append(DiscordUser(username=str(member), discord_obj=member))
        print(f'Users collected. Added {len(self.game.discord_users)} users.')
        UserUtils.print_all(self.game.discord_users)

        guild = self.guilds[0]
        text_channels = guild.text_channels
        self.game_channel = next(filter(lambda channel: channel.name == "muddle-game", text_channels), None)
        await self.send_game_chat("Server started.")
        self.game.load_players()

    def send_game_chat_sync(self, text: str, tagged_users: List[DiscordUser] = []) -> None:
        self.loop.create_task(self.send_game_chat(text, tagged_users=tagged_users))

    async def send_game_chat(self, text, tagged_users: List[DiscordUser] = []) -> None:
        if self.game_channel is None:
            print("No game channel set.")
            return
        mentions = ""
        if len(tagged_users) > 0:
            mentions = "".join(map(lambda x: "<@"+str(x.discord_obj.id)+">", tagged_users))+"\n"
        await self.game_channel.send(mentions+text)

    async def on_message(self, message: discord.Message) -> None:
        user = self.user
        author = message.author
        content = message.content
        channel = message.channel

        if author == user:  # ignore own messages
            return

        if channel != self.game_channel:
            return

        # Collect user if not in users
        discord_user = UserUtils.get_user_by_username(str(author), self.game.discord_users)
        if discord_user is None:
            print("New user found. Adding...")
            discord_user = DiscordUser(username=str(author), discord_obj=author)
            self.game.discord_user.append(discord_user)

        if not content.startswith("!"):
            return

        command_list = discord_user.get_commands(self.game)

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
                matched_command = possible_command

        if matched_command is not None:
            resp = matched_command.do_action(self.game, params, message)
            # print(f"Matched {command} to {matched_command.aliases[0]}")
            if resp is not None:
                await self.send_game_chat(resp, tagged_users=[discord_user])
            return

        if command.lower() == "get" and params[0].lower() == "ye" and params[1].lower() == "flask":
            await channel.send("You can't get ye flask")

    async def on_error(self, event, *args, **kwargs) -> None:
        with open('err.log', 'a') as f:
            if event == 'on_message':
                print("\n".join([str(x) for x in args]))
                f.write(f'Unhandled message: {args[0]}\n')
        raise


client = CustomClient(intents_contract=intents)


def run(game_ref) -> None:
    client.game = game_ref
    client.game.scheduler = Scheduler(client.loop)
    client.game.discord_connection = client
    client.run(TOKEN)
