"""This module contains the highest-level logic and only exists as a runtime aid.

Imports From:
    os

    textparser

Functions:
    main()
"""
import os

from textparser import TextParser
from summary_writer import SummaryWriter


def main() -> None:
    """Main function containing high-level logic for taking turns.

    Parameters:
        None

    Returns:
        None
    """
    USE_GRANULAR_DISPLAY = True
    BATTLES_TO_RUN = 1
    MAX_TURNS = -1
    winning_team = {"tie": 0}
    temp_battle = TextParser(f"{os.getcwd()}/battle.btl").parse()
    for team in temp_battle.teams:
        winning_team[team.name] = 0
    del temp_battle

    for i in range(BATTLES_TO_RUN):
        if BATTLES_TO_RUN > 1000:
            if i % 500 == 0:
                print(f"{((i/BATTLES_TO_RUN) * 100)}%")
        battle = TextParser(f"{os.getcwd()}/battle.btl").parse()
        battle.granular_display = USE_GRANULAR_DISPLAY
        turn_number = 1
        while len(battle.teams) >= 2:
            if battle.granular_display:
                print(f"Turn {turn_number}:")
            battle.take_battle_turn()
            turn_number += 1
            if turn_number > MAX_TURNS and MAX_TURNS != -1:
                break
        if battle.granular_display:
            if len(battle.teams) == 1:
                print(f"Team {battle.teams[0].name} is the winner.")
            else:
                print("The battle is a tie.")
            summary_writer = SummaryWriter(f"{os.getcwd()}/battle.summary")
            summary_writer.write_summary(battle)
        if len(battle.teams) != 0:
            winning_team[battle.teams[0].name] += 1
        else:
            winning_team["tie"] += 1
    if not USE_GRANULAR_DISPLAY:
        print(winning_team)


if __name__ == "__main__":
    main()
