from __future__ import annotations
import names
from typing import Optional, List
import random

import Game
from game_objects.CombatEntity import CombatEntity
from game_objects.Items.Armor import Armor, Gambeson
from game_objects.LootTable import LootTable
from utils.CombatHelpers import sum_resistances, assign_damage
from utils.Dice import roll


class Character(CombatEntity):
    from game_objects.Commands.Command import Command

    def __init__(self, name: str = None):
        super().__init__()
        from game_objects.Room import Room
        from discord_objects.DiscordUser import DiscordUser
        if name is None:
            self.name: str = names.get_full_name(gender='male')
        else:
            self.name: str = name
        self.current_room: Optional[Room] = None
        self.zone: str = "Labrynth"
        self.skills: CharacterSkills = CharacterSkills()
        self.inventory: CharacterInventory = CharacterInventory()
        self.discord_user: Optional[DiscordUser] = None
        self.max_health: int = 100
        self.health: int = 100
        self.max_stamina: int = 100
        self.stamina: int = 100
        self.max_mana: int = 100
        self.mana: int = 100
        self.actions: int = 2
        self.base_resistances: dict = {
            "hit": {},
            "dmg": {}
        }
        self.assign_damage = assign_damage

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
            "base_resistances": self.base_resistances
        }

    @classmethod
    def from_dict(cls, game, source_dict) -> Character:
        from discord_objects.DiscordUser import UserUtils
        new_char = Character(name=source_dict["name"])
        new_char.zone = source_dict["zone"]
        new_char.skills = CharacterSkills.from_dict(source_dict["skills"])
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

    @property
    def resistances(self) -> dict:  # TODO Define a type for this
        to_return = self.base_resistances.copy()
        equipment = filter(lambda x: isinstance(x, Armor), self.inventory.equipment.values())
        for item in equipment:
            to_return["hit"] = sum_resistances(to_return["hit"], item.hit_resistances)
            to_return["dmg"] = sum_resistances(to_return["dmg"], item.damage_resistances)
        return to_return

    @property
    def initiative(self) -> int:
        return roll(1, 20, advantage=1)

    @property
    def combat_name(self) -> str:
        return self.name

    def cleanup(self, game: Game):
        import os
        # Remove from
        #   game
        #   combat
        #   discord_user
        game.players.remove(self)
        if self.current_room.combat is not None:
            self.current_room.combat.players.remove(self)
        self.discord_user.current_character = None
        os.remove(f"savefiles/characters/{self.name}.json")

    def get_commands(self) -> List[Command]:
        if self.dead:
            return []
        from game_objects.Commands.CombatCommands.PassCommand import PassCommand
        from game_objects.Commands.Command import CharacterCommand, LookCommand
        from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
        from game_objects.Commands.NoncombatCommands.NoncombatCommand import NoncombatCommand
        # TODO add a character sheet command
        to_return = [CharacterCommand(), PassCommand(), LookCommand()]
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


class CharacterInventory:
    from game_objects.Commands.Command import Command
    from game_objects.Items.Item import Item
    from game_objects.Items.Equipment import Equipment

    def __init__(self):
        from game_objects.Items.Weapon import Sword, Dagger, Mace, Spear, Axe, Torch
        self.equipment = {
            "head": None,
            "body": Gambeson(),
            "offhand": None,
            "mainhand": random.choice([Sword(), Dagger(), Mace(), Spear(), Axe(), Torch()]),
            "belt": None
        }
        self.bag = []

    def to_dict(self):
        return {}

    @classmethod
    def from_dict(cls, source_dict):
        return CharacterInventory()

    def get_bag_item_by_name(self, item_name: str) -> Optional[Item]:
        matched_item = next(filter(lambda x: x.name.lower() == item_name.lower(), self.bag), None)
        return matched_item

    def get_equipment_by_name(self, item_name: str) -> Optional[Equipment]:
        matched_item = next(filter(lambda x: x.name.lower() == item_name.lower(), self.equipment.values()), None)
        return matched_item

    def equip_item(self, item: Equipment, slot_name: str) -> (bool, str):
        from game_objects.Items.Equipment import Equipment
        slot_name = slot_name.lower()
        if slot_name not in self.equipment.keys():
            return False, "Invalid Slot Name"
        if not isinstance(item, Equipment):
            return False, "Item is not an equipment"
        if item.slot == "hand" and slot_name not in ["offhand", "mainhand"]:
            return False, "Equipment cannot go in that slot"
        if item.slot == "head" and slot_name != "head":
            return False, "Equipment cannot go in that slot"
        if item.slot == "body" and slot_name != "body":
            return False, "Equipment cannot go in that slot"
        # TODO check if specified item can be equipped to the named slot
        if item.quantity > 1:
            to_equip = item.take_count_from_stack(1)
        else:
            to_equip = item
            self.bag.remove(item)
        self.unequip_item(slot_name)
        self.equipment[slot_name] = to_equip
        return True, None

    def unequip_item(self, slot_name: str) -> (bool, str):
        slot_name = slot_name.lower()
        if slot_name not in self.equipment.keys():
            return False, "Invalid Slot Name"
        if self.equipment[slot_name] is None:
            return False, "Slot is already empty."
        to_add_to_bag = self.equipment[slot_name]
        self.equipment[slot_name] = None
        self.add_item_to_bag(to_add_to_bag)
        return True, None

    def add_item_to_bag(self, to_add: Item) -> None:
        for item in self.bag:
            if item.able_to_join(to_add):
                item.quantity += to_add.quantity
                return
        self.bag.append(to_add)

    def get_commands(self) -> List[Command]:
        from game_objects.Commands.Command import InventoryCommand
        from game_objects.Commands.NoncombatCommands.UnequipCommand import Unequip
        from game_objects.Commands.NoncombatCommands.EquipCommand import Equip
        from game_objects.Commands.PartialCombatCommands.DropCommand import Drop
        from game_objects.Items.Equipment import Equipment
        to_return = [InventoryCommand()]
        if len(self.bag) > 0:
            to_return.append(Drop())
        if any(x is not None for x in self.equipment.values()):
            to_return.append(Unequip())
        if any(isinstance(x, Equipment) for x in self.bag):
            to_return.append(Equip())
        for slot in self.equipment.keys():
            if self.equipment.get(slot, None) is not None:
                to_return.extend(self.equipment.get(slot).get_commands())
        return to_return

    def generate_loot_table(self) -> LootTable:
        all_items = self.bag + list(filter(lambda x: x is not None, self.equipment))
        item_count = len(all_items)
        loot_table_items = map(lambda x: (x, 1/item_count), all_items)
        return LootTable(loot_table_items)


class CharacterSpells:
    from game_objects.Commands.Command import Command

    def __init__(self):
        self.known_spells = []

    def to_dict(self):
        return {}

    def get_commands(self) -> List[Command]:
        return []


class CharacterSkills:
    from game_objects.Commands.Command import Command

    def __init__(self):
        pass

    def to_dict(self):
        return {}

    @classmethod
    def from_dict(cls, source_dict):
        return CharacterSkills()

    def get_commands(self) -> List[Command]:
        return []


