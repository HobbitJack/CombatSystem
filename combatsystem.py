import os
import copy

from weapon import Weapon
from defense import Defense
from ship import Ship
from fleet import Fleet
from battle import Battle


def text_parser(battle_file: str) -> Battle:
    with open(battle_file, encoding="utf8") as file:
        reading: str = "None"
        weapons: dict[str, Weapon] = {}
        defenses: dict[str, Defense] = {}
        ships: dict[str, Ship] = {}
        fleets: dict[str, Fleet] = {}
        teams: dict[str, list[Fleet]] = {}
        for line in file.readlines():
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
                    weapons[line.split(":")[0]] = Weapon(
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
                if reading == "Defenses":
                    defenses[line.split(":")[0]] = Defense(
                        line.split(":")[0],
                        line.split(":")[1].split(",")[0],
                        True if line.split(":")[1].split(",")[1] == "True" else False,
                    )
                if reading == "Ships":
                    ships[line.split(":")[0]] = Ship(
                        line.split(":")[0],
                        [
                            int(line.split(":")[1].split(",")[0][1:-1].split(";")[i])
                            for i in range(3)
                        ],
                        int(line.split(":")[1].split(",")[1]),
                        [
                            weapons[
                                str(
                                    line.split(":")[1].split(",")[2][1:-1].split(";")[i]
                                )
                            ]
                            for i in range(
                                len(line.split(":")[1].split(",")[2][1:-1].split(";"))
                            )
                        ]
                        if (
                            len(line.split(":")[1].split(",")[2][1:-1].split(";")) > 1
                            or (
                                len(line.split(":")[1].split(",")[2][1:-1].split(";"))
                                == 1
                                and not (
                                    ""
                                    == line.split(":")[1]
                                    .split(",")[2][1:-1]
                                    .split(";")[0]
                                )
                            )
                        )
                        else [],
                        [
                            defenses[
                                str(
                                    line.split(":")[1].split(",")[3][1:-1].split(";")[i]
                                )
                            ]
                            for i in range(
                                len(line.split(":")[1].split(",")[3][1:-1].split(";"))
                            )
                        ]
                        if (
                            len(line.split(":")[1].split(",")[3][1:-1].split(";")) > 1
                            or (
                                len(line.split(":")[1].split(",")[3][1:-1].split(";"))
                                == 1
                                and not (
                                    ""
                                    == line.split(":")[1]
                                    .split(",")[3][1:-1]
                                    .split(";")[0]
                                )
                            )
                        )
                        else [],
                    )
                if reading == "Fleets":
                    all_ships = [
                        line.split(":")[1][1:-2].split(";")[i].split("|")[0]
                        for i in range(len(line.split(":")[1][1:-2].split(";")))
                        for _ in range(
                            int(line.split(":")[1][1:-1].split(";")[i].split("|")[1])
                        )
                    ]
                    fleets[line.split(":")[0]] = Fleet(
                        line.split(":")[0],
                        [
                            copy.deepcopy(ships[all_ships[i]])
                            for i in range(len(all_ships))
                        ],
                    )
                if reading == "Teams":
                    teams[line.split(":")[0]] = [
                        fleets[line.split(":")[1][1:-1].split(";")[i]]
                        for i in range(len(line.split(":")[1][1:-1].split(";")))
                    ]
        return Battle(teams)


battle = text_parser(f"{os.getcwd()}/battle.btl")

turn_number = 1
while all([len(battle.teams[key]) for key in battle.teams]):
    print(f"Turn {turn_number}:")
    battle.take_battle_turn()
    turn_number += 1
print([len(battle.teams[key]) for key in battle.teams])
input()
