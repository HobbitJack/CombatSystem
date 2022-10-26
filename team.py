from dataclasses import dataclass
from fleet import Fleet


@dataclass
class Team:
    name: int
    fleets: list[Fleet]
    team_number: int
