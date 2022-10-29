"""This class stores the dataclass used to store data for defenses

Imports From:
    dataclasses

Classes:
    Defense
"""
from dataclasses import dataclass


@dataclass
class Defense:
    """Stores the data for each defense.

    Attributes:
        name: str | Human-readable name for this weapon.
        hit_function: str | Hit function determining how many weapons this defense will stop
        is_area_defense: bool | Determines if this defense is an area defense or not.

    Methods:
        None
    """

    name: str
    hit_function: str
    is_area_defense: bool
