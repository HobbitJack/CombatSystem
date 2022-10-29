"""
This module contains the Battle class, which has the logic for taking battle turns and
the high-level logic done when sending weapons around

Imports From:
    random

    fleet
    team

Classes:
    Battle
"""
import random

from fleet import Fleet
from team import Team


class Battle:
    """This class contains all teams in the battle, and the logic for running turns.

    Attributes:
        teams: list[Team] | List of all teams in this battle.

    Methods:
        calculate_sensors()
        fire_weapons()
        take_battle_turn()
    """

    def __init__(self, teams: list[Team]) -> None:
        self.teams = teams

    def __str__(self) -> str:
        return_string = ""
        for team in self.teams:
            return_string += f"{team.name}: {team.fleets}\n"
        return return_string

    def calculate_sensors(self, sensor_fleet: Fleet, sensor_team: Team) -> None:
        """Calculate sensor logic, TMA, and LINK

        Parameters:
            sensor_fleet: Fleet | The fleet for which TMA is being calculated.
            sensor_team: Team | The team which sensor_fleet belongs to.

        Returns:
            None
        """

        # We only will do sensor stuff for other teams' vessels
        all_fleets_from_other_teams: list[Fleet] = [
            fleet
            for team in self.teams
            for fleet in team.fleets
            if team.team_number != sensor_team.team_number
        ]

        # No activity counter; we only count up if nothing has happened
        if len(sensor_fleet.detected_fleets) == 0 and len(sensor_fleet.tma_fleets) == 0:
            sensor_fleet.no_activity_counter += 1
        else:
            sensor_fleet.no_activity_counter = 0

        # If we're at three turns without activity, go active (ensures combat always happens)
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

        # Calculate LINK; Passive fleets can recieve
        for fleet in sensor_team.link_fleets:
            if fleet not in sensor_fleet.detected_fleets:
                sensor_fleet.detected_fleets.append(fleet)

        # Only active fleets can send LINK data
        if sensor_fleet.is_active:
            for fleet in sensor_fleet.detected_fleets:
                if fleet not in sensor_team.link_fleets:
                    sensor_team.link_fleets.append(fleet)

    def fire_weapons(self, fleet: Fleet) -> None:
        """Make each ship in the fleet fire its weapons

        Parameters:
            fleet: Fleet | The fleet to fire weapons from.

        Returns:
            None
        """
        # Each ship fires at a random fleet
        for ship in fleet.ships:
            target_fleet = (
                random.choice(fleet.detected_fleets)
                if len(fleet.detected_fleets) > 0
                else False
            )
            # If we've actually got someone to shoot at
            if isinstance(target_fleet, Fleet):
                for weapon in ship.weapons:
                    # If we have ammo
                    if weapon.total_turns > 0 or weapon.total_turns == -1:
                        # UNLOAD!!!!
                        for _ in range(weapon.shots_per_turn):
                            target_fleet.incoming_weapons.append(weapon)
                        # Remove expended ammo
                        if weapon.total_turns > 0:
                            weapon.total_turns -= 1

    def remove_dead_ships(self) -> None:
        """Remove all dead ships and killed teams

        Parameters:
            None

        Returns:
            None
        """
        # Initialize list of dead teams
        teams_to_remove = []
        # Loop every every ship in every fleet to see if it's dead
        for team in self.teams:
            for fleet in team.fleets:
                # Initialize ships to kill for each fleet
                ships_to_remove: list[int] = []
                for i, ship in enumerate(fleet.ships):
                    # If the hull is compromised, the ship is dead
                    if ship.damage[2] <= 0:
                        ships_to_remove.append(i)

                # Sort it so that we remove the correct ship
                ships_to_remove.sort(reverse=True)
                for ship_id in ships_to_remove:
                    fleet.ships.pop(ship_id)

                # If the fleet is killed, remove it
                if len(fleet.ships) == 0:
                    team.fleets.remove(fleet)

                # Recalcluate area defenses based on killed ships
                fleet.recalculate_area_defenses()

            # If there are no fleets left for a team, that team is dead
            if len(team.fleets) == 0:
                teams_to_remove.append(team.team_number)

        # Sort in reverse to ensure we don't change the order as we remove
        teams_to_remove.sort(reverse=True)
        for team_number in teams_to_remove:
            self.teams.pop(team_number)

    def take_battle_turn(self) -> None:
        """High level logic for each battle turn.

        Parameters:
            None

        Returns:
            None
        """
        # Calculate sensors
        for team in self.teams:
            for fleet in team.fleets:
                self.calculate_sensors(fleet, team)

        # Fire weapons
        for team in self.teams:
            for fleet in team.fleets:
                self.fire_weapons(fleet)

        # Calculate area defense and assign weapons
        for team in self.teams:
            for fleet in team.fleets:
                fleet.calculate_area_defenses()
                fleet.attack_vessels()

        # Calculate damage
        for team in self.teams:
            for fleet in team.fleets:
                for ship in fleet.ships:
                    ship.self_defense()
                    ship.will_be_hit_by_weapons()

        # Remove all dead ships
        self.remove_dead_ships()
