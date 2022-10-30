"""
This module contains the Fleet class, which stores individual
ships and controls AI and area defense.

Imports From:
    math
    random

    defense
    weapon
    ship

Classes:
    Fleet
"""
import math
import random

from defense import Defense
from weapon import Weapon
from ship import Ship


class Fleet:
    """This class stores the data for a fleet, including the ships in

    Attributes:
        name: str | Human-readable name for this fleet.
        ships: list[Ship] | List of all ships in this fleet.
        area_defenses: list[Defense] | All area defenses in this fleet.
        incoming_weapons: list[Weapon] | The list of all weapons aimed at this fleet.
        is_stealth: bool | Determines if this fleet is stealthy or not.
        is_active: bool | Determines if this fleet will use active sensors or not.
        detected_fleets: list[Fleet] | The list of all fleets this fleet can fire at.
        tma_fleets: dict[Fleet, int] | The list of fleets which are currently being tracked.
        no_activity_counter: int | A counter for a time period of no activity.
    """

    def __init__(self, name: str, ships: list[Ship]) -> None:
        self.name = name
        self.ships = ships
        self.area_defenses: list[Defense] = [
            ship.defenses[defense]
            for ship in self.ships
            for defense in range(len(ship.defenses))
            if ship.defenses[defense].is_area_defense
        ]
        self.incoming_weapons: list[Weapon] = []
        self.is_stealth: bool = True
        for ship in ships:
            if ship.stealth is False:
                self.is_stealth = False

        self.is_active: bool = not self.is_stealth
        self.detected_fleets: list[Fleet] = []
        self.tma_fleets: dict[Fleet, int] = {}
        self.no_activity_counter = 0

    def calculate_area_defenses(self) -> None:
        """Calculate all area defenses for this fleet.

        Parameters:
            None

        Returns:
            None
        """
        # Make the lists of interceptable and non-interceptable weapons
        interceptable_weapons = [
            weapon for weapon in self.incoming_weapons if weapon.is_interceptable
        ]
        noninterceptable_weapons = [
            weapon for weapon in self.incoming_weapons if not weapon.is_interceptable
        ]
        # Area defense is calcuated differently than point defense
        # Multiple ships can target the same incomings
        kill_list: list[int] = []
        for defense in self.area_defenses:
            # Each defense gets its own kill list
            defense_kill_list = []
            # x is the input to the damage function
            x = len(interceptable_weapons)
            weapons_killed = math.floor(
                # Eval is a necessary evil.
                eval(defense.hit_function)
                * (random.randint(10, 100) / 100)
            )
            # Each individual defense won't overlap with itself
            for _ in range(weapons_killed):
                if (target := random.randint(0, x - 1)) not in defense_kill_list:
                    defense_kill_list.append(target)

            # Defenses can overlap, though.
            for i in defense_kill_list:
                if i not in kill_list:
                    kill_list.append(i)

        # Randomize the order of the weapons
        random.shuffle(interceptable_weapons)
        unintercepted_weapons = []
        # Basically flipping the kill list
        for i, weapon in enumerate(interceptable_weapons):
            if i not in kill_list:
                unintercepted_weapons.append(weapon)

        # The weapons sent to the ships are the ones we didn't get and the ones we can't get
        self.incoming_weapons = unintercepted_weapons + noninterceptable_weapons

    def recalculate_area_defenses(self) -> None:
        """Recalculate area defenses based on remaining ships

        Parameters:
            None

        Returns:
            None
        """
        self.area_defenses = [
            ship.defenses[defense]
            for ship in self.ships
            for defense in range(len(ship.defenses))
            if ship.defenses[defense].is_area_defense
        ]

    def attack_vessels(self) -> None:
        """Distribute weapons which have made it past area defenses among ships in the fleet evenly

        Parameters:
            None

        Returns:
            None
        """
        # Set the fleet to use active if they're fired on, since they've been detected
        if len(self.incoming_weapons) > 0 and len(self.detected_fleets) == 0:
            self.is_active = True
        # Randomize the order of incoming weapons so that they are assigned randomly
        random.shuffle(self.incoming_weapons)
        # Determine the number of weapons given to each ship
        # Considering randomly distributing them?
        while len(self.incoming_weapons) > 0:
            random.choice(self.ships).incoming_weapons.append(
                self.incoming_weapons.pop()
            )

    def __str__(self) -> str:
        return_string = self.name.upper()
        all_ships: dict[str, int] = {}
        for ship in self.ships:
            if ship.name in all_ships:
                all_ships[ship.name] += 1
            else:
                all_ships[ship.name] = 1
        for ship_class, number in all_ships.items():
            return_string += f"\n{ship_class}: {number}"
        return return_string
