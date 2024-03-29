from __future__ import annotations
import discord
import random
from typing import Any, Optional

import Game
from game_objects.Commands.Command import Command
from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand
import utils.TriggerFunc
from utils.CombatHelpers import sum_resistances


class CharacterSkills:
    from game_objects.Commands.Command import Command
    from game_objects.Character.Character import Character

    def __init__(self, source_character: Character):
        self.current_character = source_character
        cartography = CartographySkill(self.current_character)
        cartography.level = 1
        combat_sense = CombatSense(self.current_character)
        combat_sense.level = 1
        dungeon_lore = DungeonLore(self.current_character)
        dungeon_lore.level = 1
        appraise = Appraise(self.current_character)
        appraise.level = 1
        self.skill_entries = {"Cartography": cartography, "CombatSense": combat_sense, "DungeonLore": dungeon_lore, "Appraise": appraise}

    def get_by_name(self, name: str) -> CharacterSkill:
        return next(filter(lambda x: x.name == name, self.skill_entries.values()), None)

    def setup_triggers(self, game: Game) -> None:
        for skill in self.skill_entries.values():
            skill.setup_triggers(game)

    def add_proficiency(self, skill_name, amount) -> None:
        pass

    def to_dict(self) -> dict:
        return {}

    @classmethod
    def from_dict(cls, source_dict, character) -> CharacterSkills:
        return CharacterSkills(character)

    def get_commands(self, game) -> list[Command]:
        to_return = []
        for name, skill in self.skill_entries.items():
            to_return = to_return + skill.get_commands()
        return to_return


class CharacterSkill(object):
    def __init__(self, source_character):
        self.current_character = source_character
        self.name: str = ""
        self.level: int = 0
        self.proficiency: int = 0
        self.proficiency_milestones = {}
        self.data = {}

    def add_proficiency(self, amount):
        pass

    def setup_triggers(self, game: Game) -> None:
        pass

    def get_commands(self):
        return []


class CartographySkill(CharacterSkill):
    from game_objects.Room import Room
    from game_objects.Character.Character import Character

    def __init__(self, source_character):
        super().__init__(source_character)
        self.name = "Cartography"

    def setup_triggers(self, game: Game) -> None:
        # TODO on maze reset, clear visited rooms
        game.on("maze_reset", utils.TriggerFunc.TriggerFunc(self.clear_visited_rooms))
        if self.level >= 1:
            game.on("enter_room", utils.TriggerFunc.TriggerFunc(self.add_to_map))

    def clear_visited_rooms(self, **kwargs) -> None:
        self.data["visited_rooms"] = []

    def add_to_map(self, source_player: Character, room: Optional[Room] = None, **kwargs) -> None:
        if source_player != self.current_character:
            return
        if "visited_rooms" in self.data.keys():
            self.data["visited_rooms"].append(room)
        else:
            self.data["visited_rooms"] = [room]
        self.proficiency = self.proficiency + 1


class CombatSense(CharacterSkill):
    def __init__(self, source_character):
        super().__init__(source_character)
        self.name = "CombatSense"

    def get_commands(self):
        return [SizeUpCommand()]


class SizeUpCommand(Command):
    from game_objects.CombatEntity import CombatEntity

    def __init__(self):
        super().__init__()
        self.aliases = ["Sizeup"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Look around the room",
            "Params:",
            "   0: Name of the enemy to size up"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        from utils.ListHelpers import get_by_index
        from utils.Constanats import DamageTypes

        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        enemies = player.current_room.combat.enemies
        target = None
        if len(params) > 0:
            from utils.CommandHelpers import match_enemy
            match_enemy_result = match_enemy(enemies, params)
            if match_enemy_result is not None:
                target = match_enemy_result
            if target is None:
                return "Specified enemy not found."
        elif len(enemies) == 1:
            target = enemies[0]
        if target is None:
            return "No enemy specified. Usage is:\n" + SizeUpCommand.show_help()
        else:
            resistances = target.resistances
            hit_resistances = resistances["hit"]
            dmg_resistances = resistances["dmg"]
            min_hit_resistance = min([hit_resistances.get(DamageTypes.Slash, 0),
                                      hit_resistances.get(DamageTypes.Pierce, 0),
                                      hit_resistances.get(DamageTypes.Bludgeon, 0)])
            min_dmg_resistance = min([dmg_resistances.get(DamageTypes.Slash, 0),
                                      dmg_resistances.get(DamageTypes.Pierce, 0),
                                      dmg_resistances.get(DamageTypes.Bludgeon, 0)])
            relevant_types = [DamageTypes.Slash, DamageTypes.Pierce, DamageTypes.Bludgeon]
            lowest_hit_resistance = random.choice([x for x in relevant_types if hit_resistances.get(x, 0) == min_hit_resistance])
            lowest_dmg_resistance = random.choice([x for x in relevant_types if dmg_resistances.get(x, 0) == min_dmg_resistance])
            damage_percent_index = (target.health * 100) // target.max_health // 20
            health_percentile_strings = {
                0: "It's barely clinging to life.",
                1: "It's badly hurt.",
                2: "It has taken quite a few hits and seems weakened.",
                3: "It's taken a few hits, but it seems to still have plenty of strength.",
                4: "It seems mostly unhurt.",
                5: "It's completely unharmed."
            }
            best_hit_strings = {
                DamageTypes.Bludgeon: "It looks like it might be easiest to hit with a bludgeoning weapon.",
                DamageTypes.Slash: "It looks like it might be easiest to hit with a slashing weapon.",
                DamageTypes.Pierce: "It looks like it might be easiest to hit with a piercing weapon."
            }
            best_dmg_strings = {
                DamageTypes.Bludgeon: "It looks like it might be weak to bludgeoning damage.",
                DamageTypes.Slash: "It looks like it might be weak to slashing damage.",
                DamageTypes.Pierce: "It looks like it might be weak to piercing damage."
            }
            resp_strings = [
                f"You eye {target.combat_name} closely.",
                health_percentile_strings[damage_percent_index],
                best_hit_strings[lowest_hit_resistance],
                best_dmg_strings[lowest_dmg_resistance]
            ]
            return "\n".join(resp_strings)


class DungeonLore(CharacterSkill):
    def __init__(self, source_character):
        super().__init__(source_character)
        self.name = "DungeonLore"

    def get_commands(self):
        return [LookupCommand()]


class LookupCommand(Command):
    def __init__(self):
        super().__init__()
        self.aliases = ["Lookup"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Look up the enemy in your dungeon guide",
            "Dev Note: This will eventually cost an action if used in combat",
            "Params:",
            "   0: Name of the enemy to look up"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:
        from discord_objects.DiscordUser import UserUtils
        from utils.ListHelpers import get_by_index
        from utils.Constanats import DamageTypes

        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        enemy_name = get_by_index(params, 0, None)
        if enemy_name is None:
            return "No enemy specified. Usage is:\n" + SizeUpCommand.show_help()
        player = discord_user.current_character
        room = player.current_room
        from utils.CommandHelpers import match_enemy, match_player
        enemies = [x for x in game.enemies if x.current_room == room]
        target = None
        match_enemy_result = match_enemy(enemies, params)
        if match_enemy_result is not None:
            target = match_enemy_result
        if target is None:
            return "Specified enemy not found."
        else:
            # list max health
            # for each damage type in damage-types
            # list hit resistance and damage resistance
            # grid with spacing of 15, left aligned, right pad to length of 15
            max_health = target.max_health
            hit_resistances = sum_resistances(target.natural_armor["hit"], target.armor_bonus["hit"])
            dmg_resistances = sum_resistances(target.natural_armor["dmg"], target.armor_bonus["dmg"])
            resp_strings = [
                f"You quickly thumb through your copy of Ogres and Oubliettes: A Field Guide and find the entry for {target.name}",
                f"Health: {max_health}",
                "Type".ljust(15)+"Hit Resist".ljust(15)+"Dmg Resist".ljust(15)
            ]
            for type in ["slash", "pierce", "bludgeon", "electricity", "fire", "ice"]:
                resp_strings.append(type.capitalize().ljust(15)+f"{hit_resistances.get(type,0 )}".ljust(15)+f"{dmg_resistances.get(type,0)}".ljust(15))

            return resp_strings[0] +  "```"+"\n".join(resp_strings[1:])+"```"


class Appraise(CharacterSkill):
    def __init__(self, source_character):
        super().__init__(source_character)
        self.name = "Appraise"

    def get_commands(self):
        return [AppraiseCommand()]


class AppraiseCommand(NoncombatCommand):
    def __init__(self):
        super().__init__()
        self.aliases = ["Appraise"]

    @classmethod
    def show_help(cls) -> str:
        return "\n".join([
            "Evaluates an item, revealing details about its apparent quality and value",
            "Params:",
            "  0: Name of an item in your bag"
        ])

    def do_action(self, game: Game, params: list[str], message: discord.Message) -> str:

        from discord_objects.DiscordUser import UserUtils
        from utils.ListHelpers import get_by_index

        discord_user = UserUtils.get_user_by_username(str(message.author), game.discord_users)
        player = discord_user.current_character
        item_name = get_by_index(params, 0, None)
        if item_name is None:
            return "Item name not specified. Usage is:\n" + AppraiseCommand.show_help()
        matched_item = player.inventory.get_bag_item_by_name(item_name)
        if matched_item is None:
            return "Item not found"

        ret_string = "You carefully examine your "+item_name+".\n"
        ret_string += quality_string(matched_item.quality)+"\n"
        ret_string += condition_string(matched_item.condition/matched_item.quality)+"\n"
        ret_string += f"You figure you could get about {appraise_value(matched_item)} gold for this."

        return ret_string


def quality_string(quality_score: int):
    quality_strings = {
        "legendary": "This item is of unbelievable quality.",  # 100
        "masterwork": "This item is of masterful quality.",  # 90-99
        "excellent": "This item is truly excellent. ",  # 80-89
        "great": "This item is really well put together.",  # 70-79
        "good": "This item looks pretty well-made.",  # 60-69
        "normal": "This item looks okay. Not bad, but not great either.",  # 40-59
        "poor": "This item looks like it was put together by an amateur or someone who wasn't having a great day. It'll probably work, but it's not something you'd choose to use if given the choice.",
        # 21-39
        "awful": "It looks like someone tried to craft this item while blindfolded and drunk. Either that or it's a joke. It's hard to believe that someone actually put any amount of effort into this."
        # 0-20
    }
    if quality_score == 100:
        return quality_strings["legendary"]
    if quality_score >= 90:
        return quality_strings["masterwork"]
    if quality_score >= 80:
        return quality_strings["excellent"]
    if quality_score >= 70:
        return quality_strings["great"]
    if quality_score >= 60:
        return quality_strings["good"]
    if quality_score >= 40:
        return quality_strings["normal"]
    if quality_score >= 20:
        return quality_strings["poor"]
    return quality_strings["awful"]


def condition_string(condition_pct: float):
    condition_strings = {
        "full_repair": "This item is in full repair.",
        "good": "This item is in very good condition.",
        "normal": "This item is in respectable condition.",
        "poor": "This item is pretty heavily worn.",
        "near-broken": "This item is on its last legs and could break at any moment."
    }
    if condition_pct == 1:
        return condition_strings["full_repair"]
    if condition_pct >= .75:
        return condition_strings["good"]
    if condition_pct >= .5:
        return condition_strings["normal"]
    if condition_pct >= .25:
        return condition_strings["poor"]
    return condition_strings["near-broken"]


def appraise_value(item):
    return item.value