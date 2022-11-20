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
        self.weapons: dict[str, Weapon] = {}
        self.defenses: dict[str, Defense] = {}
        self.ships: dict[str, Ship] = {}
        self.fleets: dict[str, Fleet] = {}
        self.teams: list[Team] = []

    def parse(self) -> Battle:
        """Parse the imported battle file and return a Battle.

        Returns:
            Battle | A Battle made from the parsed data.
        """

        reading = ""

        for line in self.imported_battle:
            # Remove extra whitespace
            line = "".join(line.split())

            # Skip the line if it is a comment or is blank
            if line.startswith("#") or line == "":
                continue
            else:
                # Different types of parsers. Switch parser when each header is detected
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

                # Run the correct parser based on what section is being read
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

    def weapon_parser(self, line: str) -> Weapon:
        """Parse the passed-in line as a weapon.

        Parameters:
            line: str | The line to be parsed as a weapon.

        Returns:
            Weapon | The parsed weapon.
        """
        return Weapon(
            # Name
            line.split(":")[0],
            # Damage Functions
            [
                (
                    # Number of dice
                    int(
                        line.split(":")[1][1:-1]
                        .split(";")[i]
                        .split("|")[0]
                        .split("d")[0]
                    ),
                    # Max roll on dice
                    int(
                        line.split(":")[1][1:-2]
                        .split(";")[i]
                        .split("|")[0]
                        .split("d")[1]
                    ),
                    # Damage function
                    line.split(":")[1][1:-1]
                    .split(",")[0][:-1]
                    .split(";")[i]
                    .split("|")[1],
                )
                for i in range(3)
            ],
            # Determine if the weapon is guided
            True if (line.split(":")[1].split(",")[1]) == "True" else False,
            # Shots per turn
            int(line.split(":")[1].split(",")[2]),
            # Total Turns
            int(line.split(":")[1].split(",")[3]),
            # Determine if the weapon is interceptable
            True if (line.split(":")[1].split(",")[4]) == "True" else False,
        )

    def defense_parser(self, line: str) -> Defense:
        """Parse the passed-in line as a defense.

        Parameters:
            line: str | The line to be parsed as a defense.

        Returns:
            Defense | The parsed defense.
        """
        return Defense(
            # Name
            line.split(":")[0],
            # Probability of Kill
            int(line.split(":")[1].split(",")[0]),
            # Min Kill
            int(line.split(":")[1].split(",")[1]),
            # Determines if the defense is an area defense
            True if line.split(":")[1].split(",")[2] == "True" else False,
        )

    def ship_parser(self, line: str) -> Ship:
        """Parse the passed-in line as a ship. I'm really sorry about this one.

        Parameters:
            line: str | The line to be parsed as a ship.

        Returns:
            Ship | The parsed ship.
        """
        return Ship(
            # Ship Name
            line.split(":")[0],
            # Ship shield, armor, and hull
            [
                int(line.split(":")[1].split(",")[0][1:-1].split(";")[i])
                for i in range(3)
            ],
            # Ship evasion stat
            int(line.split(":")[1].split(",")[1]),
            # Weapons, can be empty
            [
                self.weapons[str(line.split(":")[1].split(",")[2][1:-1].split(";")[i])]
                for i in range(len(line.split(":")[1].split(",")[2][1:-1].split(";")))
            ]
            # Ensure weapons list isn't empty while making original list
            if (
                len(line.split(":")[1].split(",")[2][1:-1].split(";")) > 1
                or (
                    len(line.split(":")[1].split(",")[2][1:-1].split(";")) == 1
                    and not ("" == line.split(":")[1].split(",")[2][1:-1].split(";")[0])
                )
            )
            # Weapons list is empty
            else [],
            # Defenses, can be empty
            [
                self.defenses[str(line.split(":")[1].split(",")[3][1:-1].split(";")[i])]
                for i in range(len(line.split(":")[1].split(",")[3][1:-1].split(";")))
            ]
            # Ensure defenses list isn't empty while making original list
            if (
                len(line.split(":")[1].split(",")[3][1:-1].split(";")) > 1
                or (
                    len(line.split(":")[1].split(",")[3][1:-1].split(";")) == 1
                    and not ("" == line.split(":")[1].split(",")[3][1:-1].split(";")[0])
                )
            )
            # Defenses list is empty
            else [],
            # Stealth factor, which will not suffice to just use an int for
            int(line.split(":")[1].split(",")[4])
            if line.split(":")[1].split(",")[4] != "False"
            else False,
        )

    def fleet_parser(self, line: str) -> Fleet:
        """Parse the passed-in line as a fleet.

        Parameters:
            line: str | The line to be parsed as a fleet.

        Returns:
            Fleet | The parsed fleet.
        """
        # Take the parsed fleet ship list and turn it into a very long and flat list of each ship
        all_ships = [
            line.split(":")[1][1:-2].split(";")[i].split("|")[0]
            for i in range(len(line.split(":")[1][1:-2].split(";")))
            for _ in range(int(line.split(":")[1][1:-1].split(";")[i].split("|")[1]))
        ]
        return Fleet(
            # Fleet name
            line.split(":")[0],
            # Ships as parsed above; deepcopy necessary to avoid re-referencing the same ship
            [copy.deepcopy(self.ships[all_ships[i]]) for i in range(len(all_ships))],
        )

    def team_parser(self, line: str) -> Team:
        """Parse the passed-in line as a team.

        Parameters:
            line: str | The line to be parsed as a team.

        Returns:
            Team | The parsed team.
        """
        return Team(
            # Team name
            line.split(":")[0],
            # Parsing each fleet in the list
            [
                self.fleets[line.split(":")[1][1:-1].split(";")[i]]
                for i in range(len(line.split(":")[1][1:-1].split(";")))
            ],
            # Assign team number as an ID; could be arbitrary and only used to avoid friendly fire
            len(self.teams),
            # LINK Fleets starts empty, but Team is a dataclass so needs a constructor argument
            [],
        )
