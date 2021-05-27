from __future__ import annotations
from typing import Dict


def load_npc_from_template(filename) -> 'NPC':
    import json
    from game_objects.NPC import NPC
    with open(f"templates/npcs/{filename}.json", "r") as infile:
        source_dict = json.load(infile)
        to_return = NPC.from_dict(source_dict)
        return to_return


def load_item_from_template(filename) -> 'Item':
    import json
    from game_objects.Items.Armor import Armor
    from game_objects.Items.Item import Item, Coins
    from game_objects.Items.Equipment import Equipment
    from game_objects.Items.Weapon import Weapon, Sword, Torch, Dagger, Mace, Spear, Axe
    with open(f"templates/items/{filename}.json", "r") as infile:
        source_dict = json.load(infile)
        constructor = source_dict.pop("constructor")
        source_dict.pop("guid")
        constructors = {
            "Weapon": Weapon,
            "Sword": Sword,
            "Torch": Torch,
            "Dagger": Dagger,
            "Mace": Mace,
            "Spear": Spear,
            "Axe": Axe,
            "Armor": Armor,
            "Item": Item,
            "Equipment": Equipment,
            "Coins": Coins
        }
        if constructor in constructors.keys():
            return constructors[constructor].from_dict(source_dict)


def save_item_template(item: 'Item') -> None:
    import json
    print(f"Writing to templates/items/{item.name}")
    with open(f"templates/items/{item.name}.json", "w") as outfile:
        json.dump(item.to_dict(full_depth=True), outfile, indent=4)


def item_mappings() -> Dict[str, 'Item']:
    from game_objects.Items.Armor import Armor, PlateArmor, ChainArmor, Gambeson
    from game_objects.Items.Weapon import Sword, Torch, Dagger, Mace, Spear, Axe, Weapon, DuelistDagger, WerebatFang, RavensBeak, PerunsPike, CrudgelOfChione
    from game_objects.Items.Shield import Shield
    from game_objects.Items.Consumables.HealthPotion import HealthPotion
    from game_objects.Items.Consumables.ManaPotion import ManaPotion
    from game_objects.Items.Consumables.StaminaPotion import StaminaPotion
    from game_objects.Items.Consumables.RagePotion import RagePotion
    from game_objects.Items.Consumables.FocusPotion import FocusPotion

    from game_objects.Items.Item import Item, Coins, DungeonMap
    return {
        "Armor": Armor,
        "PlateArmor": PlateArmor,
        "ChainArmor": ChainArmor,
        "Gambeson": Gambeson,
        "Sword": Sword,
        "Torch": Torch,
        "Dagger": Dagger,
        "DuelistDagger": DuelistDagger,
        "WerebatFang": WerebatFang,
        "RavensBeak": RavensBeak,
        "Mace": Mace,
        "CrudgelOfChione": CrudgelOfChione,
        "PerunsPike": PerunsPike,
        "Spear": Spear,
        "Axe": Axe,
        "Item": Item,
        "Coins": Coins,
        "Weapon": Weapon,
        "Shield": Shield,
        "HealthPotion": HealthPotion,
        "StaminaPotion": StaminaPotion,
        "FocusPotion": FocusPotion,
        "RagePotion": RagePotion,
        "ManaPotion": ManaPotion,
        "DungeonMap": DungeonMap
    }


def generate_item_templates() -> None:
    from game_objects.Items.Armor import Armor, PlateArmor, ChainArmor, Gambeson
    from game_objects.Items.Weapon import Sword, Torch, Dagger, Mace, Spear, Axe, DuelistDagger, WerebatFang, PerunsPike, CrudgelOfChione, RavensBeak
    from game_objects.Items.Shield import Shield
    from game_objects.Items.Consumables.HealthPotion import HealthPotion
    from game_objects.Items.Consumables.ManaPotion import ManaPotion
    from game_objects.Items.Consumables.StaminaPotion import StaminaPotion
    to_write = [
        Armor(),
        PlateArmor(),
        ChainArmor(),
        Gambeson(),
        Sword(),
        Torch(),
        Dagger(),
        DuelistDagger(),
        WerebatFang(),
        Mace(),
        RavensBeak(),
        CrudgelOfChione(),
        Spear(),
        Axe(),
        PerunsPike(),
        Shield(),
        HealthPotion(),
        ManaPotion(),
        StaminaPotion()
    ]
    for item in to_write:
        save_item_template(item)
    print("Regenerated Item Templates")


if __name__ == "__main__":
    generate_item_templates()
