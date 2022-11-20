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
        probability_kill: int = {0, 100} | The probability that this defense kills the next weapon.
        min_kill: int | The minimum number of incoming weapons this defense will always kill.
        is_area_defense: bool | Determines if this defense is an area defense or not.

    Methods:
        None
    """

    name: str
    probability_kill: int
    min_kill: int
    is_area_defense: bool
