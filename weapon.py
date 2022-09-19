from dataclasses import dataclass


@dataclass
class Weapon:
    name: str
    damage_functions: list[tuple[int, int, str]]
    is_guided: bool
    shots_per_turn: int
    total_turns: int
    is_interceptable: bool
