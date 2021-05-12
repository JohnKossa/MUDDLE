from __future__ import annotations
import random
from typing import Optional, List


class CharacterInventory:
    from game_objects.Commands.Command import Command
    from game_objects.Items.Item import Item
    from game_objects.Items.Equipment import Equipment
    from game_objects.LootTable import LootTable

    def __init__(self):
        from game_objects.Items.Armor import Gambeson
        from game_objects.Items.Weapon import Sword, Dagger, Mace, Spear, Axe, Torch
        from game_objects.Items.Consumables.HealthPotion import HealthPotion
        from game_objects.Items.Item import Item
        self.equipment = {
            "head": None,
            "body": Gambeson(),
            "offhand": None,
            "mainhand": random.choice([Sword(), Dagger(), Mace(), Spear(), Axe(), Torch()]),
            "belt": [HealthPotion()]
        }
        self.bag: List[Item] = [HealthPotion()]

    def to_dict(self) -> dict:
        to_return = {
            "equipment": {},
            "bag": []
        }
        for k, v in self.equipment.items():
            if v is not None and k != "belt":
                to_return["equipment"][k] = v.to_dict()
            elif k == "belt":
                to_return["equipment"]["belt"] = []
                for item in self.equipment["belt"]:
                    to_return["equipment"]["belt"].append(item.to_dict())
        for item in self.bag:
            to_return["bag"].append(item.to_dict())
        return to_return

    @classmethod
    def from_dict(cls, source_dict) -> CharacterInventory:
        from templates.TemplateLoaders import item_mappings
        constructors = item_mappings()

        to_return = CharacterInventory()
        to_return.equipment = {
            "head": None,
            "body": None,
            "offhand": None,
            "mainhand": None,
            "belt": []
        }
        for k, v in source_dict["equipment"].items():
            if k != "belt":
                constructor_name = v.pop("constructor")
                to_return.equipment[k] = constructors.get(constructor_name).from_dict(v)
            elif k == "belt":
                for item in source_dict["equipment"]["belt"]:
                    constructor_name = item.pop("constructor")
                    to_return.equipment["belt"].append(constructors.get(constructor_name).from_dict(item))
        to_return.bag = []
        for item in source_dict["bag"]:
            constructor_name = item.pop("constructor")
            to_return.add_item_to_bag(constructors.get(constructor_name).from_dict(item))
        return to_return

    def get_belt_item_by_name(self, item_name: str) -> Optional[Item]:
        matched_item = next(filter(lambda x: x.name.lower() == item_name.lower(), self.equipment["belt"]), None)
        return matched_item

    def get_bag_item_by_name(self, item_name: str) -> Optional[Item]:
        matched_item = next(filter(lambda x: x.name.lower() == item_name.lower(), self.bag), None)
        return matched_item

    def get_equipment_by_name(self, item_name: str) -> Optional[Equipment]:
        matched_item = next(filter(lambda x: x.name.lower() == item_name.lower(), self.equipment.values()), None)
        return matched_item

    def consolidate_items(self) -> None:
        from game_objects.Items.Item import Item
        consolidation_made: bool = True
        while consolidation_made:
            consolidation_made = False
            for i in range(len(self.bag)):
                first_item: Item = self.bag[i]
                remaining_items: List[Item] = self.bag[i+1:]
                for ii in range(len(remaining_items)):
                    second_item: Item = remaining_items[ii]
                    if first_item.able_to_join(second_item):
                        first_item.quantity = first_item.quantity + second_item.quantity
                        self.bag.remove(second_item)
                        consolidation_made = True
                        break
                if consolidation_made:
                    break

    def equip_item(self, item: Item, slot_name: str) -> (bool, str):
        from game_objects.Items.Equipment import Equipment
        from game_objects.Items.Consumables.Consumable import Consumable
        slot_name = slot_name.lower()
        if slot_name not in self.equipment.keys():
            return False, "Invalid Slot Name"
        if slot_name == "belt":
            if not isinstance(item, Consumable):
                return False, "Cannot equip that item to belt."
            else:
                self.add_item_to_belt(item)
                self.bag.remove(item)
                return True, None
        if not isinstance(item, Equipment) and slot_name in ["offhand", "mainhand", "head", "body"]:
            return False, "Item is not an equipment"
        if item.slot == "hand" and slot_name not in ["offhand", "mainhand"]:
            return False, "Equipment cannot go in that slot"
        if item.slot == "head" and slot_name != "head":
            return False, "Equipment cannot go in that slot"
        if item.slot == "body" and slot_name != "body":
            return False, "Equipment cannot go in that slot"
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
        if slot_name != "belt" and self.equipment[slot_name] is None:
            return False, "Slot is already empty."
        if slot_name == "belt":
            if len(self.equipment["belt"]) == 0:
                return False, "Slot is already empty."
            else:
                for item in self.equipment["belt"]:
                    self.add_item_to_bag(item)
                self.equipment["belt"] = []
                return True, None
        else:
            to_add_to_bag = self.equipment[slot_name]
            self.equipment[slot_name] = None
            self.add_item_to_bag(to_add_to_bag)
            return True, None

    def add_item_to_belt(self, to_add: Item) -> None:
        for item in self.equipment["belt"]:
            if item.able_to_join(to_add):
                item.quantity += to_add.quantity
                return
        self.equipment["belt"].append(to_add)

    def add_item_to_bag(self, to_add: Item) -> None:
        for item in self.bag:
            if item.able_to_join(to_add):
                item.quantity += to_add.quantity
                return
        self.bag.append(to_add)

    def get_commands(self, game) -> List[Command]:
        from game_objects.Commands.Command import Command
        from game_objects.Commands.StaticCommands.InventoryCommand import InventoryCommand
        from game_objects.Commands.NoncombatCommands.UnequipCommand import Unequip
        from game_objects.Commands.NoncombatCommands.EquipCommand import Equip
        from game_objects.Commands.PartialCombatCommands.DropCommand import Drop
        from game_objects.Commands.PartialCombatCommands.UseItemCommand import UseItem
        from game_objects.Items.Equipment import Equipment
        from game_objects.Items.Consumables.Consumable import Consumable
        to_return: List[Command] = [InventoryCommand()]
        if len(self.bag) > 0:
            to_return.append(Drop())
        if any(x is not None for x in self.equipment.values()):
            to_return.append(Unequip())
        if any(isinstance(x, Equipment) for x in self.bag) or any(isinstance(x, Consumable) for x in self.bag):
            to_return.append(Equip())
        if any(isinstance(x, Consumable) for x in self.bag + self.equipment["belt"]):
            to_return.append(UseItem())
        for slot in self.equipment.keys():
            if slot == "belt":
                for item in self.equipment["belt"]:
                    to_return = to_return + item.get_commands(game)
                continue
            if self.equipment.get(slot, None) is not None:
                to_return = to_return + self.equipment.get(slot).get_commands(game)
        return to_return

    def generate_loot_table(self) -> LootTable:
        from game_objects.LootTable import LootTable
        all_items = self.bag + list(filter(lambda x: x is not None, self.equipment.values()))
        loot_table_items = map(lambda x: (x, .5), all_items)
        return LootTable(loot_table_items)