from __future__ import annotations
import names
from typing import Optional, List

import Game

from game_objects.CombatEntity import CombatEntity
from game_objects.GameEntity import GameEntity
from utils.CombatHelpers import sum_resistances, assign_damage
from utils.Dice import roll


class Character(CombatEntity, GameEntity):
    from game_objects.Commands.Command import Command

    def __init__(self, name: str = None):
        super().__init__()
        from game_objects.Room import Room
        from discord_objects.DiscordUser import DiscordUser
        from game_objects.Character.CharacterInventory import CharacterInventory
        from game_objects.Character.CharacterSkills import CharacterSkills
        if name is None:
            self.name: str = names.get_full_name(gender='male')
        else:
            self.name: str = name
        self.current_room: Optional[Room] = None
        self.zone: str = "Labrynth"
        self.skills: CharacterSkills = CharacterSkills(self)
        self.inventory: CharacterInventory = CharacterInventory()
        self.discord_user: Optional[DiscordUser] = None
        self.max_health: int = 100
        self.health: int = 100
        self.max_stamina: int = 100
        self.stamina: int = 100
        self.max_mana: int = 100
        self.mana: int = 100
        self.actions: int = 2
        self.luck: int = 0
        self.base_resistances: dict = {
            "hit": {},
            "dmg": {}
        }
        self.status_effects = []
        self.assign_damage = assign_damage

    @property
    def resistances(self) -> dict:  # TODO Define a type for this
        from game_objects.Items.Armor import Armor
        to_return = self.base_resistances.copy()
        equipment = filter(lambda x: isinstance(x, Armor), self.inventory.equipment.values())
        for item in equipment:
            to_return["hit"] = sum_resistances(to_return["hit"], item.hit_resistances)
            to_return["dmg"] = sum_resistances(to_return["dmg"], item.damage_resistances)
        for status in self.status_effects:
            to_return["hit"] = sum_resistances(to_return["hit"], status.hit_resistances)
            to_return["dmg"] = sum_resistances(to_return["dmg"], status.dmg_resistances)
        return to_return

    @property
    def initiative(self) -> int:
        return roll(1, 20, advantage=1)

    @property
    def combat_name(self) -> str:
        return self.name

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "zone": self.zone,
            "skills": self.skills.to_dict(),
            "inventory": self.inventory.to_dict(),
            "discord_user": self.discord_user.username,
            "health": self.health,
            "max_health": self.max_health,
            "stamina": self.stamina,
            "max_stamina": self.max_stamina,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "actions": self.actions,
            "luck": self.luck,
            "base_resistances": self.base_resistances
        }

    @classmethod
    def from_dict(cls, game, source_dict) -> Character:
        from discord_objects.DiscordUser import UserUtils
        from game_objects.Character.CharacterInventory import CharacterInventory
        from game_objects.Character.CharacterSkills import CharacterSkills
        new_char = Character(name=source_dict["name"])
        new_char.zone = source_dict["zone"]
        new_char.skills = CharacterSkills.from_dict(source_dict["skills"], new_char)
        new_char.inventory = CharacterInventory.from_dict(source_dict["inventory"])
        new_char.discord_user = UserUtils.get_user_by_username(source_dict["discord_user"], game.discord_users)
        new_char.health = source_dict["health"]
        new_char.max_health = source_dict["max_health"]
        new_char.stamina = source_dict["stamina"]
        new_char.max_stamina = source_dict["max_stamina"]
        new_char.mana = source_dict["mana"]
        new_char.max_mana = source_dict["max_mana"]
        new_char.actions = source_dict["actions"]
        new_char.base_resistances = source_dict["base_resistances"]
        return new_char

    def initialize(self, game: Game) -> None:
        self.skills.setup_triggers(game)

    def cleanup(self, game: Game) -> None:
        import os
        game.players_dict.pop(self.guid)
        if self.current_room.combat is not None:
            if self in self.current_room.combat.players:
                self.current_room.combat.players.remove(self)
        self.discord_user.current_character = None
        for status in self.status_effects:
            status.character = None
        os.remove(f"savefiles/characters/{self.name}.json")

    def get_commands(self) -> List[Command]:
        if self.dead:
            return []
        from game_objects.Commands.CombatCommands.DodgeCommand import DodgeCommand
        from game_objects.Commands.CombatCommands.PassCommand import PassCommand
        from game_objects.Commands.Command import CharacterCommand, LookCommand
        from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
        from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand
        # TODO add a character sheet command
        to_return = [CharacterCommand(), PassCommand(), LookCommand(), DodgeCommand()]
        if self.current_room is not None:
            to_return.extend(self.current_room.get_commands())
        if self.skills is not None:
            to_return.extend(self.skills.get_commands())
        if self.inventory is not None:
            to_return.extend(self.inventory.get_commands())
        # if player not in combat, remove all combat only commands
        if self.current_room.combat is None:
            to_return = list(filter(lambda x: not isinstance(x, CombatOnlyCommand), to_return))
        else:
            to_return = list(filter(lambda x: not isinstance(x, NoncombatCommand), to_return))
        return to_return

    def __str__(self):
        return self.discord_user.username+" as "+("Unnamed Player" if self.name is None else self.name)
