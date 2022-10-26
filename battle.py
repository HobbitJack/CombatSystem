import random

from fleet import Fleet
from team import Team


class Battle:
    def __init__(self, teams: list[Team]) -> None:
        self.teams = teams

    def __str__(self) -> str:
        return_string = ""
        for team in self.teams:
            return_string += f"{team.name}: {team.fleets}\n"
        return return_string

    def fire_weapons(self, fleet: Fleet, team_number: int):
        for ship in fleet.ships:
            target_fleet = random.choice(
                random.choice(
                    [
                        team.fleets
                        for team in self.teams
                        if team.team_number != team_number and len(team.fleets) > 0
                    ]
                )
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
        for team in self.teams:
            for fleet in team.fleets:
                self.fire_weapons(fleet, team.team_number)

        for team in self.teams:
            for fleet in team.fleets:
                fleet.calculate_area_defenses()
                fleet.attack_vessels()

        for team in self.teams:
            for fleet in team.fleets:
                for ship in fleet.ships:
                    ship.self_defense()
                    ship.will_be_hit_by_weapons()

        teams_to_remove = []
        for team_id, team in enumerate(self.teams):
            for fleet in team.fleets:
                ships_to_remove = []
                for i, ship in enumerate(fleet.ships):
                    if ship.damage[2] <= 0:
                        print(f"{ship.name} killed!")
                        ships_to_remove.append(i)
                ships_to_remove.sort(reverse=True)
                for ship_id in ships_to_remove:
                    fleet.ships.pop(ship_id)

                if len(fleet.ships) == 0:
                    team.fleets.remove(fleet)

                fleet.recalculate_area_defenses()

            if len(team.fleets) == 0:
                teams_to_remove.append(team_id)

        teams_to_remove.sort(reverse=True)
        for team_id in teams_to_remove:
            self.teams.pop(team_id)
