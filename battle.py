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

    def calculate_sensors(self, sensor_fleet: Fleet, sensor_team: Team):
        all_fleets_from_other_teams: list[Fleet] = [
            fleet
            for team in self.teams
            for fleet in team.fleets
            if team.team_number != sensor_team.team_number
        ]

        # No activity counter
        if len(sensor_fleet.detected_fleets) == 0 and len(sensor_fleet.tma_fleets) == 0:
            sensor_fleet.no_activity_counter += 1
        else:
            sensor_fleet.no_activity_counter = 0

        if sensor_fleet.no_activity_counter == 3:
            sensor_fleet.is_active = True

        # Calculate TMA
        for fleet in sensor_fleet.tma_fleets:
            sensor_fleet.tma_fleets[fleet] += 1
            if (
                sensor_fleet.tma_fleets[fleet] == 3
                and fleet not in sensor_fleet.detected_fleets
            ):
                sensor_fleet.detected_fleets.append(fleet)

        # Caculate sensor detection
        if sensor_fleet.is_active:
            for fleet in all_fleets_from_other_teams:
                if fleet.is_stealth:
                    for ship in fleet.ships:
                        if random.randint(1, 20) > random.randint(1, 20) + ship.stealth:
                            if fleet not in sensor_fleet.detected_fleets:
                                sensor_fleet.detected_fleets.append(fleet)
                else:
                    if fleet not in sensor_fleet.detected_fleets:
                        fleet.detected_fleets.append(fleet)

        # Calculate ESM
        for fleet in all_fleets_from_other_teams:
            if (
                fleet.is_active
                and fleet not in sensor_fleet.detected_fleets
                and fleet not in sensor_fleet.tma_fleets.keys()
            ):
                sensor_fleet.tma_fleets[fleet] = 1

        # Calculate LINK
        if sensor_fleet.is_active:
            for fleet in sensor_team.link_fleets:
                if fleet not in sensor_fleet.detected_fleets:
                    sensor_fleet.detected_fleets.append(fleet)
        for fleet in sensor_fleet.detected_fleets:
            if fleet not in sensor_team.link_fleets:
                sensor_team.link_fleets.append(fleet)

    def fire_weapons(self, fleet: Fleet):
        for ship in fleet.ships:
            target_fleet = (
                random.choice(fleet.detected_fleets)
                if len(fleet.detected_fleets) > 0
                else False
            )
            if isinstance(target_fleet, Fleet):
                for weapon in ship.weapons:
                    if weapon.total_turns > 0 or weapon.total_turns == -1:
                        for _ in range(weapon.shots_per_turn):
                            target_fleet.incoming_weapons.append(weapon)
                        if weapon.total_turns > 0:
                            weapon.total_turns -= 1

    def take_battle_turn(self):
        # Before we do anything else, we calculate sensors
        # First, we calculate weapons fire
        # Then, we calculate area defense on fleets and assign weapons to ships
        # Then, we calculate self defense on ships
        # Then, we calcluate damage on ships
        # Finally, we calculate the remaining ships.
        for team in self.teams:
            for fleet in team.fleets:
                self.calculate_sensors(fleet, team)

        for team in self.teams:
            for fleet in team.fleets:
                self.fire_weapons(fleet)

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
