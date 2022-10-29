import math
import random
from typing import Union

from defense import Defense
from weapon import Weapon


class Ship:
    def __init__(
        self,
        name: str,
        damage: list[int],
        evasion: int,
        weapons: list[Weapon],
        defenses: list[Defense],
        stealth: Union[bool, int],
    ) -> None:
        self.name = name
        self.damage = damage
        self.evasion = evasion
        self.weapons = weapons
        self.defenses = defenses
        self.all_incoming_weapons: list[Weapon] = []
        self.incoming_weapons: list[Weapon] = []
        self.stealth = stealth

    def take_damage(self, damage: int, area: int) -> None:
        damage, self.damage[area] = (
            damage - self.damage[area] if damage > self.damage[area] else 0,
            self.damage[area] - damage if damage < self.damage[area] else 0,
        )
        if damage != 0 and area != 2:
            damage, self.damage[area + 1] = (
                damage - self.damage[area + 1] if damage > self.damage[area + 1] else 0,
                self.damage[area + 1] - damage if damage < self.damage[area + 1] else 0,
            )
            if damage != 0 and area + 1 != 2:
                self.damage[area + 2] = (
                    self.damage[area + 2] - damage
                    if damage < self.damage[area + 2]
                    else 0
                )

    def calculate_damage(self, damage_function: list[tuple[int, int, str]]) -> None:
        for area in [0, 1, 2]:
            if not (self.damage[area] <= 0 or damage_function[area][2] == "True"):
                if damage_function[area][2] == "False":
                    return
                x = sum(
                    [
                        random.randint(1, damage_function[area][1])
                        for _ in range(damage_function[area][0])
                    ]
                )
                damage: int = eval(damage_function[area][2])
                self.take_damage(damage, area)
                break
            else:
                continue

    def will_be_hit_by_weapons(self):
        for weapon in self.incoming_weapons:
            if weapon.is_guided:
                self.calculate_damage(weapon.damage_functions)
            else:
                if random.randint(1, 100) > random.randint(1, 100) + self.evasion:
                    self.calculate_damage(weapon.damage_functions)

    def self_defense(self):
        self.all_incoming_weapons = self.incoming_weapons.copy()
        for defense in self.defenses:
            if not defense.is_area_defense:
                interceptable_weapons = [
                    weapon
                    for weapon in self.incoming_weapons
                    if weapon.is_interceptable
                ]
                noninterceptable_weapons = [
                    weapon
                    for weapon in self.incoming_weapons
                    if not weapon.is_interceptable
                ]
                x = len(interceptable_weapons)
                weapons_killed = math.floor(
                    eval(defense.hit_function) * (random.randint(25, 175) / 100)
                )
                x = x - weapons_killed if x > weapons_killed else 0
                if x == 0:
                    interceptable_weapons = []
                else:
                    random.shuffle(interceptable_weapons)
                    for _ in range(len(interceptable_weapons) - x):
                        interceptable_weapons.pop()
                self.incoming_weapons = interceptable_weapons + noninterceptable_weapons
            else:
                continue

    def __str__(self) -> str:
        return_string = self.name.upper()
        return_string += f"\nShield: {self.damage[0]}"
        return_string += f"\nArmor: {self.damage[1]}"
        return_string += f"\nHull: {self.damage[2]}"
        return_string += f"\nEvasion: {self.evasion}"
        return_string += f"\nWeapons: {[weapon.name for weapon in self.weapons]}"
        return_string += f"\nDefenses: {[weapon.name for weapon in self.weapons]}"
        return return_string
