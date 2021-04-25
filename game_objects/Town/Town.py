from __future__ import annotations
from typing import List, Optional

from game_objects.Room import Room
from game_objects.Town.ApothecaryStore import ApothecaryStore
from game_objects.Town.BlacksmithShop import BlacksmithShop
from game_objects.Town.GeneralStore import GeneralStore
from game_objects.Town.HeroesGuild import HeroesGuild
from game_objects.Town.MageShop import MageShop
from game_objects.Town.TownSquare.TownSquare import TownSquare


class Town:
    def __init__(self):
        self.rooms: List[Room] = []
        self.entry_room: Optional[Room] = None
        self.generate_town()

    def get_room_by_name(self, name) -> Optional[Room]:
        return next(filter(lambda x: x.name == name, self.rooms), None)

    def generate_town(self, level: int = 0) -> None:
        town_square = TownSquare()
        apothecary = ApothecaryStore()
        blacksmith = BlacksmithShop()
        general_store = GeneralStore()
        heroes_guild = HeroesGuild()
        mage_shop = MageShop()
        self.entry_room = town_square
        self.rooms.append(town_square)
        self.rooms.append(heroes_guild)
        self.rooms.append(apothecary)
        self.rooms.append(general_store)
        self.rooms.append(blacksmith)
        self.rooms.append(mage_shop)
        apothecary.neighbors = [town_square]
        blacksmith.neighbors = [town_square]
        general_store.neighbors = [town_square]
        heroes_guild.neighbors = [town_square]
        mage_shop.neighbors = [town_square]
        town_square.neighbors = town_square.neighbors + [apothecary, blacksmith, general_store, heroes_guild, mage_shop]
