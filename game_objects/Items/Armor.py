from __future__ import annotations

from game_objects.Items.Equipment import Equipment
from utils.Constanats import DamageTypes


class Armor(Equipment):
    from game_objects.Commands.Command import Command

    def __init__(self):
        from utils.Constanats import EquipmentSlots
        super().__init__()
        self.slot: str = EquipmentSlots.Body
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.damage_resistances: dict = {}
        self.hit_resistances: dict = {}

    def to_dict(self, full_depth=True) -> dict:
        to_return = super().to_dict() if full_depth else {}
        to_add = {
            "constructor": self.__class__.__name__,
            "slot": self.slot,
            "damage_resistances": self.damage_resistances,
            "hit_resistances": self.hit_resistances
        }
        to_return.update(to_add)
        return to_return

    @classmethod
    def from_dict(cls, source_dict) -> Armor:
        to_return = Armor()
        to_return.__dict__.update(source_dict)
        return to_return

    def get_commands(self, game) -> list[Command]:
        return super().get_commands(game) + []


class PlateArmor(Armor):
    from game_objects.Commands.Command import Command

    def __init__(self):
        super().__init__()
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.name: str = "IronPlate"
        self.traits = self.traits + ["metallic"]
        self.damage_resistances: dict = {
            DamageTypes.Slash: 2,
            DamageTypes.Pierce: 0,
            DamageTypes.Bludgeon: 1,
            DamageTypes.Electricity: -5
        }
        self.hit_resistances: dict = {
            DamageTypes.Slash: 2,
            DamageTypes.Pierce: 1,
            DamageTypes.Bludgeon: 0,
            DamageTypes.Electricity: -1
        }

    def get_commands(self, game) -> list[Command]:
        return super().get_commands(game) + []


class ChainArmor(Armor):
    from game_objects.Commands.Command import Command

    def __init__(self):
        super().__init__()
        # resistances bestowed to user when equipped. assumed to be 0 if not specified
        self.name: str = "IronChainmail"
        self.traits = self.traits + ["metallic"]
        self.damage_resistances: dict = {
            DamageTypes.Slash: 2,
            DamageTypes.Pierce: 1,
            DamageTypes.Bludgeon: 1,
            DamageTypes.Electricity: -3
        }
        self.hit_resistances: dict = {
            DamageTypes.Slash: 2,
            DamageTypes.Pierce: 1,
            DamageTypes.Bludgeon: 0,
            DamageTypes.Electricity: -1
        }

    def get_commands(self, game) -> list[Command]:
        return super().get_commands(game) + []


class Gambeson(Armor):
    from game_objects.Commands.Command import Command

    def __init__(self):
        super().__init__()
        self.name: str = "Gambeson"
        self.damage_resistances: dict = {
            DamageTypes.Slash: 1,
            DamageTypes.Pierce: 0,
            DamageTypes.Bludgeon: 2,
            DamageTypes.Electricity: 2,
            DamageTypes.Ice: 2,
            DamageTypes.Fire: -1,
        }
        self.hit_resistances: dict = {
            DamageTypes.Slash: 1,
            DamageTypes.Pierce: 0,
            DamageTypes.Bludgeon: 0,
            DamageTypes.Electricity: 0,
            DamageTypes.Ice: 0,
            DamageTypes.Fire: -1
        }

    def get_commands(self, game) -> list[Command]:
        return super().get_commands(game) + []
