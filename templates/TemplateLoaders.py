from game_objects.Items.Item import Item


def load_item_from_template(filename):
    import json
    from game_objects.Items.Armor import Armor
    from game_objects.Items.Item import Item, Coins
    from game_objects.Items.Equipment import Equipment
    from game_objects.Items.Weapon import Weapon, Sword, Torch, Dagger, Mace, Spear, Axe
    with open(f"templates/items/{filename}.json", "r") as infile:
        source_dict = json.load(infile)
        constructor = source_dict.pop("constructor")
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
            constructors[constructor].from_dict(source_dict)


def save_item_template(item: Item):
    import json
    print(f"Writing to templates/items/{item.name}")
    with open(f"templates/items/{item.name}.json", "w") as outfile:
        json.dump(item.to_dict(full_depth=True), outfile)


def item_mappings():
    from game_objects.Items.Armor import Armor, PlateArmor, ChainArmor, Gambeson
    from game_objects.Items.Weapon import Sword, Torch, Dagger, Mace, Spear, Axe, Weapon
    from game_objects.Items.Item import Item, Coins
    return {
        "Armor": Armor,
        "PlateArmor": PlateArmor,
        "ChainArmor": ChainArmor,
        "Gambeson": Gambeson,
        "Sword": Sword,
        "Torch": Torch,
        "Dagger": Dagger,
        "Mace": Mace,
        "Spear": Spear,
        "Axe": Axe,
        "Item": Item,
        "Coins": Coins,
        "Weapon": Weapon
    }


def generate_item_templates():
    from game_objects.Items.Armor import Armor, PlateArmor, ChainArmor, Gambeson
    from game_objects.Items.Weapon import Sword, Torch, Dagger, Mace, Spear, Axe
    from game_objects.Items.Shield import Shield
    to_write = [
        Armor(),
        PlateArmor(),
        ChainArmor(),
        Gambeson(),
        Sword(),
        Torch(),
        Dagger(),
        Mace(),
        Spear(),
        Axe(),
        Shield()
    ]
    for item in to_write:
        save_item_template(item)
    print("Regenerated Item Templates")


if __name__ == "__main__":
    generate_item_templates()
