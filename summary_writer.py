"""This module contains the summary writer for the end of battles.

Imports From:
    os

    weapon
    defense
    ship
    fleet
    battle
    team

Classes:
    SummaryWriter
"""
import os

from battle import Battle


class SummaryWriter:
    def __init__(self, file_directory: str) -> None:
        if os.path.exists(file_directory):
            os.remove(file_directory)
        self.file_directory = file_directory

    def write_summary(self, battle: Battle):
        with open(self.file_directory, mode="a", encoding="utf8") as file:
            for team in battle.teams:
                file.write(f"{team.name}:\n")
                for fleet in team.fleets:
                    file.write(f"{fleet.name}:\n")
                    for ship in fleet.ships:
                        file.write(f"{ship.name}: {ship.damage}\n")
                        for weapon in ship.weapons:
                            file.write(
                                f"{weapon.name}: Shots Left: {weapon.total_turns}\n"
                            )
                        file.write("\n")
                    file.write("\n")
                file.write("\n")
            file.close()
