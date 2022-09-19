import random

from fleet import Fleet


class Battle:
    def __init__(self, teams: dict[str, list[Fleet]]) -> None:
        self.teams = teams

    def __str__(self) -> str:
        return_string = ""
        for team_name, team_fleets in self.teams.items():
            return_string += f"{team_name}: {team_fleets}\n"
        return return_string

    def fire_weapons(self, fleet: Fleet, fleet_team: str):
        for ship in fleet.ships:
            target_fleet = random.choice(
                self.teams[
                    random.choice(
                        [
                            team[0]
                            for team in self.teams.items()
                            if team[0] != fleet_team
                        ]
                    )
                ]
            )
            for weapon in ship.weapons:
                if weapon.total_turns > 0:
                    for _ in range(weapon.shots_per_turn):
                        target_fleet.incoming_weapons.append(weapon)
                    weapon.total_turns -= 1

    def take_battle_turn(self):
        # First, we calculate weapons fire
        # Then, we calculate area defense on fleets and assign weapons to ships
        # Then, we calculate self defense on ships
        # Then, we calcluate damage on ships
        # Finally, we calculate the remaining ships.
        for team in self.teams.items():
            for fleet in team[1]:
                self.fire_weapons(fleet, team[0])

        for team in self.teams.items():
            for fleet in team[1]:
                fleet.calculate_area_defenses()
                fleet.attack_vessels()

        for team in self.teams.items():
            for fleet in team[1]:
                for ship in fleet.ships:
                    ship.self_defense()
                    ship.will_be_hit_by_weapons()

        for team in self.teams.items():
            for fleet in team[1]:
                ships_to_remove = []
                for i, ship in enumerate(fleet.ships):
                    if ship.damage[2] <= 0:
                        print(f"{ship.name} killed!")
                        ships_to_remove.append(i)
                ships_to_remove.sort(reverse=True)
                for i in ships_to_remove:
                    fleet.ships.pop(i)

                if len(fleet.ships) == 0:
                    team[1].remove(fleet)
                fleet.redo_area_defenses()
