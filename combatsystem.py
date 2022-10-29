"""This module contains the highest-level logic and only exists as a runtime aid.

Imports From:
    os

    textparser

Functions:
    main()
"""
import os

from textparser import TextParser


def main() -> None:
    """Main function containing high-level logic for taking turns.

    Parameters:
        None

    Returns:
        None
    """
    battle = TextParser(f"{os.getcwd()}/battle.btl").parse()

    turn_number = 1
    while len(battle.teams) >= 2:
        print(f"Turn {turn_number}:")
        battle.take_battle_turn()
        turn_number += 1

    if len(battle.teams) == 1:
        print(f"Team {battle.teams[0].name} is the winner.")
    else:
        print("The battle is a tie.")


if __name__ == "__main__":
    main()
