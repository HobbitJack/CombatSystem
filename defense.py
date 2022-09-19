from dataclasses import dataclass


@dataclass
class Defense:
    name: str
    hit_function: str
    is_area_defense: bool
