from dataclasses import dataclass
from fleet import Fleet


@dataclass
class Team:
    name: str
    fleets: list[Fleet]
    team_number: int
    link_fleets: list[Fleet]
