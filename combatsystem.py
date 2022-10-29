import os

from textparser import TextParser


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
