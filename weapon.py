"""This module contains the class used to store weapons.

Imports From:
    dataclasses

Classes:
    Weapon
"""
from dataclasses import dataclass


@dataclass
class Weapon:
    """Stores the data for each weapon.

    Attributes:
        name: str | Human-readable name for this weapon.
        damage_functions: list[tuple[int, int, str]] | #dice, dice max number, and damage function.
        is_guided: bool | Determines if this weapon is guided and thus always hits.
        shots_per_turn: int | The number of weapons fired by this weapon per turn.
        total_turns: int | The total number of turns this weapon can fire for.
        is_interceptable: bool | Determines if this weapon can be intercepted by defenses.

    Methods:
        None
    """

    name: str
    damage_functions: list[tuple[int, int, str]]
    is_guided: bool
    shots_per_turn: int
    total_turns: int
    is_interceptable: bool
