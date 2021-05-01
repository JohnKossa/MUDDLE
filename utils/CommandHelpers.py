from typing import Any, List, Optional
import discord

from game_objects.Character.Character import Character
from game_objects.Items.Item import Item
from game_objects.Enemy import Enemy
from game_objects.NPC import NPC


def match_bag_item(player: Character, params: List[str], message: discord.Message) -> Optional[Item]:
    raise Exception("Not Implemented")


def match_enemy(enemy_list: List[Enemy], params: List[Any]) -> Optional[Enemy]:
    for enemy in enemy_list:
        if enemy.combat_name.lower() == params[0].lower():
            return enemy
    return None


def match_player(player_list: List[Character], params: List[Any]) -> Optional[Character]:
    for player in player_list:
        if player.combat_name.lower() == params[0].lower():
            return player
    return None

def match_npc(npc_list: List[NPC], params: List[Any]) -> Optional[NPC]:
    return None
