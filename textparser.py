"""This module contains the text parser for battle files.

Imports From:
    copy

    weapon
    defense
    ship
    fleet
    battle
    team

Classes:
    TextParser
"""
import copy

from weapon import Weapon
from defense import Defense
from ship import Ship
from fleet import Fleet
from battle import Battle
from team import Team


class TextParser:
    """Class which exists to parse text

    Attributes:
        reading: str = "None" | Stores which type of data is being read.
        weapons: dict[str, Weapon] = {} | Stores all read weapons.
        defenses: dict[str, Defense] = {} | Stores all read defenses.
        ships: dict[str, Ship] = {} | Stores all read ships.
        fleets: dict[str, Fleet] = {} | Stores all read fleets.
        teams: list[Team] = [] | Stores all read teams.

    Methods:
        parse()
        weapon_parser()
        defense_parser()
        ship_parser()
        fleet_parser()
        team_parser()
    """

    def __init__(self, file_directory: str) -> None:
        with open(file_directory, mode="r", encoding="utf8") as file:
            self.imported_battle = file.readlines()
        self.reading: str = "None"
        self.weapons: dict[str, Weapon] = {}
        self.defenses: dict[str, Defense] = {}
        self.ships: dict[str, Ship] = {}
        self.fleets: dict[str, Fleet] = {}
        self.teams: list[Team] = []

    def parse(self) -> Battle:
        for line in self.imported_battle:
            line = "".join(line.split())
            if line.startswith("#") or line == "":
                continue
            else:
                if line.startswith("[WEAPONS]"):
                    reading = "Weapons"
                    continue
                if line.startswith("[DEFENSES]"):
                    reading = "Defenses"
                    continue
                if line.startswith("[SHIPS]"):
                    reading = "Ships"
                    continue
                if line.startswith("[FLEETS]"):
                    reading = "Fleets"
                    continue
                if line.startswith("[TEAMS]"):
                    reading = "Teams"
                    continue

                if reading == "Weapons":
                    self.weapons[line.split(":")[0]] = self.weapon_parser(line)
                if reading == "Defenses":
                    self.defenses[line.split(":")[0]] = self.defense_parser(line)
                if reading == "Ships":
                    self.ships[line.split(":")[0]] = self.ship_parser(line)
                if reading == "Fleets":
                    self.fleets[line.split(":")[0]] = self.fleet_parser(line)
                if reading == "Teams":
                    self.teams.append(self.team_parser(line))
        return Battle(self.teams)

    def weapon_parser(self, line: str):
        return Weapon(
            line.split(":")[0],
            [
                (
                    int(
                        line.split(":")[1][1:-1]
                        .split(";")[i]
                        .split("|")[0]
                        .split("d")[0]
                    ),
                    int(
                        line.split(":")[1][1:-2]
                        .split(";")[i]
                        .split("|")[0]
                        .split("d")[1]
                    ),
                    line.split(":")[1][1:-1]
                    .split(",")[0][:-1]
                    .split(";")[i]
                    .split("|")[1],
                )
                for i in range(3)
            ],
            True if (line.split(":")[1].split(",")[1]) == "True" else False,
            int(line.split(":")[1].split(",")[2]),
            int(line.split(":")[1].split(",")[3]),
            True if (line.split(":")[1].split(",")[4]) == "True" else False,
        )

    def defense_parser(self, line: str):
        return Defense(
            line.split(":")[0],
            line.split(":")[1].split(",")[0],
            True if line.split(":")[1].split(",")[1] == "True" else False,
        )

    def ship_parser(self, line):
        return Ship(
            line.split(":")[0],
            [
                int(line.split(":")[1].split(",")[0][1:-1].split(";")[i])
                for i in range(3)
            ],
            int(line.split(":")[1].split(",")[1]),
            [
                self.weapons[str(line.split(":")[1].split(",")[2][1:-1].split(";")[i])]
                for i in range(len(line.split(":")[1].split(",")[2][1:-1].split(";")))
            ]
            if (
                len(line.split(":")[1].split(",")[2][1:-1].split(";")) > 1
                or (
                    len(line.split(":")[1].split(",")[2][1:-1].split(";")) == 1
                    and not ("" == line.split(":")[1].split(",")[2][1:-1].split(";")[0])
                )
            )
            else [],
            [
                self.defenses[str(line.split(":")[1].split(",")[3][1:-1].split(";")[i])]
                for i in range(len(line.split(":")[1].split(",")[3][1:-1].split(";")))
            ]
            if (
                len(line.split(":")[1].split(",")[3][1:-1].split(";")) > 1
                or (
                    len(line.split(":")[1].split(",")[3][1:-1].split(";")) == 1
                    and not ("" == line.split(":")[1].split(",")[3][1:-1].split(";")[0])
                )
            )
            else [],
            int(line.split(":")[1].split(",")[4])
            if line.split(":")[1].split(",")[4] != "False"
            else False,
        )

    def fleet_parser(self, line: str):
        all_ships = [
            line.split(":")[1][1:-2].split(";")[i].split("|")[0]
            for i in range(len(line.split(":")[1][1:-2].split(";")))
            for _ in range(int(line.split(":")[1][1:-1].split(";")[i].split("|")[1]))
        ]
        return Fleet(
            line.split(":")[0],
            [copy.deepcopy(self.ships[all_ships[i]]) for i in range(len(all_ships))],
        )

    def team_parser(self, line: str):
        return Team(
            line.split(":")[0],
            [
                self.fleets[line.split(":")[1][1:-1].split(";")[i]]
                for i in range(len(line.split(":")[1][1:-1].split(";")))
            ],
            len(self.teams),
            [],
        )
