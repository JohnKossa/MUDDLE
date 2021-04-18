from __future__ import annotations
import random
from typing import List, Optional

import Game
from game_objects.Room import Room
from game_objects.Town.ApothecaryStore import ApothecaryStore
from game_objects.Town.BlacksmithShop import BlacksmithShop
from game_objects.Town.DonationBox import DonationBox
from game_objects.Town.GeneralStore import GeneralStore
from game_objects.Town.HeroesGuild import HeroesGuild
from game_objects.Town.MageShop import MageShop
from game_objects.Town.TownSquare import TownSquare


class Town:
    def __init__(self):
        self.rooms: List[Room] = []
        self.entry_room: Optional[Room] = None
        self.generate_town()

    def generate_town(self, level: int = 0):
        town_square = TownSquare()
        donation_box = DonationBox()
        apothecary = ApothecaryStore()
        blacksmith = BlacksmithShop()
        general_store = GeneralStore()
        heroes_guild = HeroesGuild()
        mage_shop = MageShop()
        self.rooms.append(town_square)
        self.entry_room = town_square
        self.rooms.append(donation_box)
        donation_box.neighbors.append(town_square)
        self.rooms.append(apothecary)
        apothecary.neighbors.append(town_square)
        self.rooms.append(blacksmith)
        blacksmith.neighbors.append(town_square)
        self.rooms.append(general_store)
        general_store.neighbors.append(town_square)
        self.rooms.append(heroes_guild)
        heroes_guild.neighbors.append(town_square)
        self.rooms.append(mage_shop)
        mage_shop.neighbors.append(town_square)
        town_square.neighbors = town_square.neighbors + [donation_box, apothecary, blacksmith, general_store, heroes_guild, mage_shop]
