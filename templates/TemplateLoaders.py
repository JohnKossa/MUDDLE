from game_objects.Items.Item import Item


def load_item_from_template(filename):
    import json
    from game_objects.Items.Armor import Armor
    from game_objects.Items.Item import Item
    from game_objects.Items.Equipment import Equipment
    from game_objects.Items.Weapon import Weapon, Sword, Torch, Dagger, Mace, Spear, Axe
    with open("templates/items/" + filename, "r") as infile:
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
            "Equipment": Equipment
        }
        if constructor in constructors.keys():
            constructors[constructor].from_dict(source_dict)


def save_item_template(item: Item):
    import json
    print("time to write")
    with open(f"templates/items/{item.name}", "w") as outfile:
        json.dump(item.to_dict(full_depth=True), outfile)