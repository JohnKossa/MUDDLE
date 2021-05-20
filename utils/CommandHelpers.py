from typing import Any, List, Optional
import discord

from game_objects.Character.Character import Character
from game_objects.Items.Item import Item
from game_objects.Enemy import Enemy
from game_objects.NPC import NPC
from game_objects.Spells.Spell import Spell


def match_bag_item(player: Character, params: List[str]) -> Optional[Item]:
    return match_item(player.inventory.bag, params)


def match_item(item_list: List[Item], params: List[Any]) -> Optional[Item]:
    return next((item for item in item_list if item.name.lower() == params[0].lower()))


def match_enemy(enemy_list: List[Enemy], params: List[Any]) -> Optional[Enemy]:
    return next((enemy for enemy in enemy_list if enemy.combat_name.lower() == params[0].lower()), None)


def match_player(player_list: List[Character], params: List[Any]) -> Optional[Character]:
    return next((player for player in player_list if player.combat_name.lower() == params[0].lower()), None)


def match_spell(spell_list: List[Spell], params: List[Any])-> Optional[Spell]:
    return next((spell for spell in spell_list if spell.name.lower == params[0].lower()), None)


def match_npc(npc_list: List[NPC], params: List[Any]) -> Optional[NPC]:
    for npc in npc_list:
        if npc.combat_name.lower() == params[0].lower():
            return npc
    return None
