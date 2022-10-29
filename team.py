"""This module contains the class used to store team data.

Imports From:
    dataclasses

    fleet

Classes:
    Team
"""
from dataclasses import dataclass

from fleet import Fleet


@dataclass
class Team:
    """Stores the data for each team.

    Attributes:
        name: str | Human-readable name for this fleet.
        fleets: list[Fleet] | The list of each fleet belonging to this team.
        team_number: int | ID Number for this fleet; used to avoid blue-on-blue.
        link_fleets: list[Fleet] | List of all enemy fleets on this team's LINK.

    Methods:
        None
    """

    name: str
    fleets: list[Fleet]
    team_number: int
    link_fleets: list[Fleet]
