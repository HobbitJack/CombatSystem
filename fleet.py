import random
import math

from defense import Defense
from weapon import Weapon
from ship import Ship


class Fleet:
    def __init__(self, name: str, ships: list[Ship]) -> None:
        self.name = name
        self.ships = ships
        self.area_defenses: list[Defense] = [
            ship.defenses[defense]
            for ship in self.ships
            for defense in range(len(ship.defenses))
            if ship.defenses[defense].is_area_defense
        ]
        self.incoming_weapons: list[Weapon] = []
        self.all_incoming_weapons: list[Weapon] = []
        self.is_stealth = True
        for ship in ships:
            if ship.stealth is False:
                self.is_stealth = False

        self.is_active: bool = not self.is_stealth
        self.detected_fleets: list[Fleet] = []
        self.tma_fleets: dict[Fleet, int] = {}
        self.no_activity_counter = 0

    def calculate_area_defenses(self):
        self.all_incoming_weapons = self.incoming_weapons.copy()
        interceptable_weapons = [
            weapon for weapon in self.incoming_weapons if weapon.is_interceptable
        ]
        noninterceptable_weapons = [
            weapon for weapon in self.incoming_weapons if not weapon.is_interceptable
        ]
        kill_list: list[int] = []
        for defense in self.area_defenses:
            defense_kill_list = []
            x = len(interceptable_weapons)
            weapons_killed = math.floor(
                eval(defense.hit_function) * (random.randint(10, 100) / 100)
            )
            for _ in range(weapons_killed):
                if (target := random.randint(1, x)) not in defense_kill_list:
                    defense_kill_list.append(target)
            for i in defense_kill_list:
                if i not in kill_list:
                    kill_list.append(i)
        random.shuffle(interceptable_weapons)
        unintercepted_weapons = []
        for i, weapon in enumerate(interceptable_weapons):
            if i not in kill_list:
                unintercepted_weapons.append(weapon)
        self.incoming_weapons = unintercepted_weapons + noninterceptable_weapons

    def recalculate_area_defenses(self):
        self.area_defenses = [
            ship.defenses[defense]
            for ship in self.ships
            for defense in range(len(ship.defenses))
            if ship.defenses[defense].is_area_defense
        ]

    def attack_vessels(self):
        if len(self.incoming_weapons) > 0:
            self.is_active = True
        self.all_incoming_weapons = self.incoming_weapons.copy()
        random.shuffle(self.incoming_weapons)
        weapons_per_ship: int = len(self.incoming_weapons) // len(self.ships)
        for ship in self.ships:
            for _ in range(weapons_per_ship):
                ship.incoming_weapons.append(self.incoming_weapons.pop())
        if len(self.incoming_weapons) > 0:
            for i in [
                random.randint(0, len(self.ships) - 1)
                for _ in range(len(self.incoming_weapons))
            ]:
                self.ships[i].incoming_weapons.append(self.incoming_weapons.pop())

    def __str__(self) -> str:
        return_string = self.name.upper()
        all_ships: dict[str, int] = {}
        for ship in self.ships:
            if ship.name in all_ships.keys():
                all_ships[ship.name] += 1
            else:
                all_ships[ship.name] = 1
        for ship_class, number in all_ships.items():
            return_string += f"\n{ship_class}: {number}"
        return return_string
