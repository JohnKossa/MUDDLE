import names

from game_objects.Commands.CombatCommands.CombatCommand import CombatOnlyCommand
from game_objects.Commands.CombatCommands.PassCommand import PassCommand
from game_objects.Items.Weapon import Sword, Torch
from utils.Dice import roll


class Character:
    def __init__(self, name=None):
        if name is None:
            self.name = names.get_full_name(gender='male')
        else:
            self.name = name
        self.current_room = None
        self.zone = "Labrynth"
        self.skills = CharacterSkills()
        self.inventory = CharacterInventory()
        self.discord_user = None
        self.max_health = 100
        self.health = 100
        self.max_stamina = 100
        self.stamina = 100
        self.max_mana = 100
        self.mana = 100
        self.actions = 2
        self.dead = False

    @property
    def resistances(self):
        return {
            "hit": {},
            "dmg": {}
        }

    @property
    def initiative(self):
        return roll(1, 20, advantage=1)

    def get_commands(self):
        # TODO add a character sheet command
        to_return = [PassCommand()]
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
    def __init__(self):
        self.equipment = {
            "head": None,
            "body": None,
            "offhand": Torch(),
            "mainhand": Sword(),
            "belt": None
        }
        self.bag = []

    def get_item_by_name(self, item_name):
        matched_item = next(filter(lambda x: x.name.lower() == item_name.lower(), self.bag), None)
        return matched_item

    def equip_item(self, item, slot_name):
        slot_name = slot_name.lower()
        if slot_name not in self.equipment.keys():
            return (False, "Invalid Slot Name")
        from game_objects.Items.Equipment import Equipment
        if type(item) is not Equipment and not issubclass(type(item), Equipment):
            return (False, "Item is not an equipment")
        if item.slot == "hand" and slot_name not in ["offhand", "mainhand"]:
            return (False, "Equipment cannot go in that slot")
        if item.slot == "head" and slot_name != "head":
            return (False, "Equipment cannot go in that slot")
        if item.slot == "body" and slot_name != "body":
            return (False, "Equipment cannot go in that slot")
        # TODO check if specified item can be equipped to the named slot
        if item.quantity > 1:
            to_equip = item.take_count_from_stack(1)
        else:
            to_equip = item
            self.bag.remove(item)
        self.unequip_item(slot_name)
        self.equipment[slot_name] = to_equip

    def unequip_item(self, slot_name):
        slot_name = slot_name.lower()
        if slot_name not in self.equipment.keys():
            return (False, "Invalid Slot Name")
        if self.equipment[slot_name] is not None:
            to_add_to_bag = self.equipment[slot_name]
            self.equipment[slot_name] = None
            self.add_item_to_bag(to_add_to_bag)

    def add_item_to_bag(self, to_add):
        for item in self.bag:
            if item.able_to_join(to_add):
                item.quantity += to_add.quantity
                return
        self.bag.append(to_add)

    def get_commands(self):
        from game_objects.Commands.Command import Equip, Unequip
        from game_objects.Commands.PartialCombatCommands.DropCommand import Drop
        from game_objects.Items.Equipment import Equipment
        to_return = []
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
    def __init__(self):
        pass

    def get_commands(self):
        return []


class CharacterUtils:
    @staticmethod
    def print_all(player_list):
        print(" ".join([str(x) for x in player_list]))
