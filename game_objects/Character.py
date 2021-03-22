from __future__ import annotations
import names
from typing import Optional, List


from game_objects.Items.Armor import Armor, PlateArmor, ChainArmor
from utils.CombatHelpers import sum_resistances
from utils.Dice import roll


class Character:
    from game_objects.Commands.Command import Command

    def __init__(self, name: str = None):
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
        self.dead: bool = False
        self.base_resistances: dict = {
            "hit": {},
            "dmg": {}
        }

    @property
    def resistances(self) -> dict:  # TODO Define a type for this
        to_return = self.base_resistances.copy()
        equipment = filter(lambda x: issubclass(type(x), Armor) or type(x) == Armor, self.inventory.equipment.values())
        for item in equipment:
            to_return["hit"] = sum_resistances(to_return["hit"], item.hit_resistances)
            to_return["dmg"] = sum_resistances(to_return["dmg"], item.damage_resistances)
        return to_return

    @property
    def initiative(self) -> int:
        return roll(1, 20, advantage=1)

    def get_commands(self) -> List[Command]:
        from game_objects.Commands.CombatCommands.PassCommand import PassCommand
        from game_objects.Commands.Command import CharacterCommand
        from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
        # TODO add a character sheet command
        to_return = [CharacterCommand(), PassCommand()]
        if self.current_room is not None:
            to_return.extend(self.current_room.get_commands())
        if self.skills is not None:
            to_return.extend(self.skills.get_commands())
        if self.inventory is not None:
            to_return.extend(self.inventory.get_commands())
        # if player not in combat, remove all combat only commands
        if self.current_room.combat is None:
            to_return = list(filter(lambda x: not issubclass(type(x), CombatOnlyCommand), to_return))
        return to_return

    def __str__(self):
        return self.discord_user.username+" as "+("Unnamed Player" if self.name is None else self.name)


class CharacterInventory:
    from game_objects.Commands.Command import Command
    from game_objects.Items.Item import Item
    from game_objects.Items.Equipment import Equipment

    def __init__(self):
        from game_objects.Items.Weapon import Sword, Torch
        self.equipment = {
            "head": None,
            "body": PlateArmor(),
            "offhand": None,
            "mainhand": Sword(),
            "belt": None
        }
        self.bag = [ChainArmor(), Torch()]

    def get_item_by_name(self, item_name: str) -> Optional[Item]:
        matched_item = next(filter(lambda x: x.name.lower() == item_name.lower(), self.bag), None)
        return matched_item

    def equip_item(self, item: Equipment, slot_name: str) -> (bool, str):
        from game_objects.Items.Equipment import Equipment
        slot_name = slot_name.lower()
        if slot_name not in self.equipment.keys():
            return False, "Invalid Slot Name"
        if type(item) is not Equipment and not issubclass(type(item), Equipment):
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
        from game_objects.Commands.Command import Equip, Unequip, InventoryCommand
        from game_objects.Commands.PartialCombatCommands.DropCommand import Drop
        from game_objects.Items.Equipment import Equipment
        to_return = [InventoryCommand()]
        if len(self.bag) > 0:
            to_return.append(Drop())
        if any(x is not None for x in self.equipment.values()):
            to_return.append(Unequip())
        if any(issubclass(type(x), Equipment) or (type(x) is Equipment) for x in self.bag):
            to_return.append(Equip())
        for slot in self.equipment.keys():
            if self.equipment.get(slot, None) is not None:
                to_return.extend(self.equipment.get(slot).get_commands())
        return to_return


class CharacterSkills:
    from game_objects.Commands.Command import Command

    def __init__(self):
        pass

    def get_commands(self) -> List[Command]:
        return []


