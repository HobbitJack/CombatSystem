"""
This module contains the Ship class, the class responsible for the defense and damage of each
individual ship simulated.

Imports From:
    math
    random
    typing

    defense
    weapon

Classes:
    Ship
"""

import math
import random
from typing import Union

from defense import Defense
from weapon import Weapon


class Ship:
    """This class stores all of the data for a ship and controls it being damaged and self-defense.

    Attributes:
        name: str | Human-readable name for this ship.
        damage: list[int] | List of health remaining for each of the three damage types.
        evasion: int | Evasion factor for this ship.
        weapons: list[Weapon] | List of all weapons on this ship.
        defenses: list[Defense] | List of all defenses on this ship.
        stealth: Union[bool, int] | Stealth factor for this ship; False means not stealth.

    Methods:
        take_damage()
        calculate_damage()
        will_be_hit_by_weapons()
        self_defense()
    """

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
        """Distribute incoming damage upon the hit area, and calculate bleedthrough.

        Paramters:
            damage: int | Total points of damage to be delt, starting at the specified area.
            area: int = {0, 2} | Area of the ship to be hit.

        Returns:
            None
        """
        # Set damage value either to bleedthrough or 0, and set HP value to remaining health or 0
        damage, self.damage[area] = (
            damage - self.damage[area] if damage > self.damage[area] else 0,
            self.damage[area] - damage if damage < self.damage[area] else 0,
        )
        # Do bleedthrough for the next area
        if damage != 0 and area != 2:
            damage, self.damage[area + 1] = (
                damage - self.damage[area + 1] if damage > self.damage[area + 1] else 0,
                self.damage[area + 1] - damage if damage < self.damage[area + 1] else 0,
            )
            # Bleedthrough for the last area
            if damage != 0 and area + 1 != 2:
                self.damage[area + 2] = (
                    self.damage[area + 2] - damage
                    if damage < self.damage[area + 2]
                    else 0
                )

    def calculate_damage(self, damage_function: list[tuple[int, int, str]]) -> None:
        """Determine which area on the ship needs to be hit and calcuate the damage to be applied.

        Parameters:
            damage_function: list[tuple[int, int, str]] | The dice and damage function to use.

        Returns:
            None
        """
        for area in [0, 1, 2]:
            # Check that the area isn't destroyed and that we don't bypass it
            if not (self.damage[area] <= 0 or damage_function[area][2] == "True"):
                # Some weapons do no damage against certain areas and can't penetrate them
                if damage_function[area][2] == "False":
                    return
                # "x" is the variable used in the damage functions for the sum of the dice rolls
                x = sum(
                    [
                        # Max of dice
                        random.randint(1, damage_function[area][1])
                        # Number of dice
                        for _ in range(damage_function[area][0])
                    ]
                )
                # Eval is required here. Not ideal.
                damage: int = eval(damage_function[area][2])
                self.take_damage(damage, area)
                # Ensure we don't run the loop too many times
                break
            else:
                # Move onto the next area if the current one is destroyed
                continue

    def will_be_hit_by_weapons(self) -> None:
        """Calcuates evasion for each incoming weapon

        Parameters:
            None

        Returns:
            None
        """
        # For every incoming weapon
        for weapon in self.incoming_weapons:
            # Guided weapons always hit
            if weapon.is_guided:
                self.calculate_damage(weapon.damage_functions)
            else:
                # Unguided weapons have evasion rolls
                if random.randint(1, 100) > random.randint(1, 100) + self.evasion:
                    self.calculate_damage(weapon.damage_functions)

    def self_defense(self):
        """Calculate point defense for this ship

        Parameters:
            None

        Returns:
            None
        """
        for defense in self.defenses:
            # Area defenses were already calcuated for the entire fleet
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
                # Calculate weapons killed
                num_weapons = len(interceptable_weapons)
                weapons_killed = defense.min_kill
                for _ in range(num_weapons):
                    if random.randint(0, 100) < defense.probability_kill:
                        weapons_killed += 1
                    else:
                        break
                weapons_killed = math.floor(
                    weapons_killed * (random.randint(25, 175) / 100)
                )
                # If we've killed everything, clear incoming
                num_weapons = (
                    num_weapons - weapons_killed if num_weapons > weapons_killed else 0
                )
                if num_weapons == 0:
                    interceptable_weapons = []
                else:
                    # Randomly destroy incoming weapons
                    random.shuffle(interceptable_weapons)
                    for _ in range(len(interceptable_weapons) - num_weapons):
                        interceptable_weapons.pop()
                # Reconstruct incoming weapons with the ones we can't stop and the ones we missed
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
