from typing import Any, Optional

from game_objects.Character.Character import Character
from game_objects.Items.Item import Item
from game_objects.Enemy import Enemy
from game_objects.NPC import NPC
from game_objects.Spells.Spell import Spell


def match_bag_item(player: Character, params: list[str]) -> Optional[Item]:
    return match_item(player.inventory.bag, params)


def match_item(item_list: list[Item], params: list[Any]) -> Optional[Item]:
    match = next((item for item in item_list if item.name.lower() == params[0].lower()), None)
    if match is not None:
        return match
    match = next((item for item in item_list if params[0].lower() in [x.lower() for x in item.aliases]), None)
    if match is not None:
        return match
    if len(params) == 1:
        return match
    match = next((item for item in item_list if item.name.lower() == (params[0]+" "+params[1]).lower()), None)
    if match is not None:
        return match
    match = next(
        (item for item in item_list if (params[0]+" "+params[1]).lower() in [x.lower() for x in item.aliases]),
        None)
    return match


def match_enemy(enemy_list: list[Enemy], params: list[Any]) -> Optional[Enemy]:
    return next((enemy for enemy in enemy_list if enemy.combat_name.lower() == params[0].lower()), None)


def match_player(player_list: list[Character], params: list[Any]) -> Optional[Character]:
    return next((player for player in player_list if player.combat_name.lower() == params[0].lower()), None)


def match_spell(spell_list: list[Spell], params: list[Any])-> Optional[Spell]:
    return next((spell for spell in spell_list if spell.name.lower == params[0].lower()), None)


def match_npc(npc_list: list[NPC], params: list[Any]) -> Optional[NPC]:
    for npc in npc_list:
        if npc.combat_name.lower() == params[0].lower():
            return npc
    return None
