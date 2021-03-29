import random
from typing import Optional, List

from game_objects.Items.Armor import Gambeson
from game_objects.LootTable import LootTable


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
        to_return = {
            "equipment": {},
            "bag": []
        }
        for k, v in self.equipment.items():
            if v is not None:
                to_return["equipment"][k] = v.to_dict()
        for item in self.bag:
            to_return["bag"].append(item.to_dict())
        return to_return

    @classmethod
    def from_dict(cls, source_dict):
        from templates.TemplateLoaders import item_mappings
        constructors = item_mappings()

        to_return = CharacterInventory()
        to_return.equipment = {
            "head": None,
            "body": None,
            "offhand": None,
            "mainhand": None,
            "belt": None
        }
        for k, v in source_dict["equipment"].items():
            constructor_name = v.pop("constructor")
            to_return.equipment[k] = constructors.get(constructor_name).from_dict(v)
        for item in source_dict["bag"]:
            constructor_name = item.pop("constructor")
            to_return.add_item_to_bag(constructors.get(constructor_name).from_dict(item))
        return to_return

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