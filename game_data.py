"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Any, Optional, TextIO


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: name of the item
        - start_position: the initial position of the item
        - target_position: where the item should be deposited to earn points
        - target_point: the number of points earned once the item reaches its target location

    Representation Invariants:
        - name != ''
    """
    name: str
    start_position: int
    target_position: int
    target_points: int

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - position: the position of the location in the world map
        - brief_description: a brief description of the location
        - long_description: a detailed description of the location
        - actions: a list of actions available at this location
        - items: a list of the items available at this location
        - visited_before: whether this location has been visited before
        - location_number: the number assigned to this location on the map

    Representation Invariants:
        - brief_description != ''
        - long_description != ''
    """
    position: list[int, int]
    score: int
    brief_description: str
    long_description: str
    actions: list[str]
    items: list[Item]
    visited_before: bool
    location_number: int

    def __init__(self, position: list[int, int], score: int, brief_description: str, long_description: str,
                 actions: list[str], items: list[Item], visited_before: bool, location_number: int) -> None:
        """
        Initialize a new location.
        """

        self.position = position
        self.score = score
        self.brief_description = brief_description
        self.long_description = long_description
        self.actions = actions
        self.items = items
        self.visited_before = visited_before
        self.location_number = location_number

    def available_actions(self) -> list[str]:
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """
        return self.actions

    def get_coordinates(self) -> list[int, int]:
        """
        Return the x, y coordinates of the Location based on map.txt. map_data is an open text file.
        """
        return self.position

    def get_items(self) -> list[Item]:
        """
        Return a list of Item objects currently at this location.
        """
        return self.items

    def get_number(self) -> int:
        """
        Return the location number associated with this location.
        """
        return self.location_number


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - locations: a dictionary mapping location numbers to Location objects. Corresponding Item objects will be
        associated with these Locations.

    Representation Invariants:
        - len(map) > 1
        - all([len(line) > 1 for line in map])
        - all(any(location.location_number in sublist for sublist in self.map) for location in self.locations)
        - all(0 <= location.position[0] < len(self.map[0]) and 0 <= location.position[1] < len(self.map) for
                location in self.locations)
    """
    map_data: TextIO
    location_data: TextIO
    items_data: TextIO

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """
        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)
        self.locations = self.load_locations(location_data)
        self.load_items(items_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        """

        map_loaded = []
        for line in map_data:
            line = line.strip('\n').split()
            map_loaded.append([int(number) for number in line])
        return map_loaded

    def load_locations(self, location_data: TextIO) -> dict[int: Location]:
        """
        Store location data from open file location_data into a dicionary mapping of location numbers to location
        objects, like so:

        If location_data is a file containing the following text and the location is located at [0, 1] on the map:
        LOCATION 3
        0
        Short description.
        Long description.
        Walk East
        Examine
        END
        then load_locations should assign this World object's locations to be
        {3: Location([0, 1], 0, 'Short description', 'Long description', ['Walk East', 'Examine'], [], False)}

        Return this dictionary representation of locations.
        """

        location_loaded = {}
        lines = location_data.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith("LOCATION"):
                # Assigning each instance attribute to a value in the stripped line
                location_number = int(lines[i][9:].strip())
                score = int(lines[i + 1].strip())
                short_description = lines[i + 2].strip()
                long_description = lines[i + 3].strip()

                # Loading the next few lines into a list of actions
                actions = []
                j = i + 4
                while lines[j].strip() != "END":
                    action_line = lines[j].strip()
                    if action_line:
                        actions.append(action_line)
                    j += 1
                i = j + 1  # Skip the line containing "END"

                coordinates = [0, 0]
                for y in self.map:
                    for x in y:
                        if x == location_number:
                            coordinates = [y.index(x), self.map.index(y)]
                            break

                # Assigning the instance attributes to a newly created Location object stored in the location_loaded
                # dictionary.
                location_loaded[location_number] = Location(coordinates, score, short_description, long_description,
                                                            actions, [], False, location_number)
            else:
                i += 1  # Increment i if the line does not start with "LOCATION"

        return location_loaded

    def load_items(self, items_data: TextIO) -> None:
        """
        Load items and associate them with the corresponding starting locations.
        For example, if items.txt contains the following:
        1 10 5 Cheat Sheet
        1 13 5 Pen
        Then self.locations[1].items should be a list of Item objects corresponding to Cheat Sheet and Pen.

        Does not return anything.
        """
        data = items_data.readlines()
        for line in data:
            line = line.strip().split()
            # Splitting lines in items.txt
            new_item = Item(" ". join(line[3:]), int(line[0]), int(line[1]), int(line[2]))
            # Adding different parts of the line as attributes to a new Item object
            self.locations[new_item.start_position].items.append(new_item)
            # Assigning the new Item object to its corresponding Location object in the location dictionary

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """

        location_number = self.map[y][x]
        return self.locations[location_number]


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - x: x coordinate of player. Top left corner of the map is 0. Increases going right.
        - y: y coordinate of player. Top left corner is 0. Increases going down.
        - inventory: list of Item objects currently possessed by the player.
        - victory: True if the player has won. False otherwise.
        - score: The current score of the player. Increases as more items are picked up and locations reached.
        - moves: Number of available moves left for the player.
        - world: The world in which the player exists.

    Representation Invariants:
        - x < len(self.world.map[y])
        - y < len(self.world.map)
        - score >= 0
    """
    x: int
    y: int
    inventory: list[Item]
    victory: bool
    score: int
    moves: int
    world: Optional[World]

    def __init__(self, x: int, y: int, world: World) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False
        self.score = 0
        self.moves = 20
        self.world = world

    def move(self, direction: str) -> str:
        """
        The method corresponding to movement commands. Takes in a direction "EAST", "WEST", "NORTH", "SOUTH".
        Changes the player's coordinates.
        """

        new_location = self.world.locations[-1]
        if direction.upper() == "EAST":
            if self.x + 1 < len(self.world.map[self.y]) and self.world.map[self.y][self.x + 1] != -1:
                self.x += 1
                new_location = self.world.get_location(self.x, self.y)
            else:
                print("That way is blocked.")
        elif direction.upper() == "WEST":
            if self.x - 1 >= 0 and self.world.map[self.y][self.x - 1] != -1:
                self.x -= 1
                new_location = self.world.get_location(self.x, self.y)
            else:
                print("That way is blocked.")
        elif direction.upper() == "NORTH":
            if self.y - 1 >= 0 and self.world.map[self.y - 1][self.x] != -1:
                self.y -= 1
                new_location = self.world.get_location(self.x, self.y)
            else:
                print("That way is blocked.")
        elif direction.upper() == "SOUTH":
            if self.y + 1 < len(self.world.map) and self.world.map[self.y + 1][self.x] != -1:
                self.y += 1
                new_location = self.world.get_location(self.x, self.y)
            else:
                print("That way is blocked.")
        else:
            print("That is not a valid direction!")

        self.moves -= 1
        if new_location.score != 0 and not new_location.visited_before:
            self.score += new_location.score  # Gives player scores for visiting an important location!
            print(f"You earned {new_location.score} points by visiting here.")

        print(f"You have {self.moves} moves left.")

    def get_score(self) -> None:
        """
        Print the current score of the player.
        """
        print("Your current score is: " + str(self.score))

    def get_moves(self) -> None:
        """
        Print the number of moves left.
        """
        print("You have " + str(self.moves) + " moves left.")

    def check_inventory(self) -> None:
        """
        Print information about items currently in the player's inventory.
        """
        if not self.inventory:
            print("Womp womp...There's nothing in your inventory!")
        else:
            print("In your inventory, you currently have: " + ', '.join([item.name for item in self.inventory]))

    def pickup_item(self, item_name: str) -> None:
        """
        Allows the player to pick up a specified item at the location.
        """
        for item in self.world.get_location(self.x, self.y).items:
            if item.name.upper() == item_name.upper():
                self.world.get_location(self.x, self.y).items.remove(item)
                # Remove Item object from the location
                self.inventory.append(item)
                # Add Item object to the player's inventory
                print(f"You just picked up {item.name}! It's in your bag now, check inventory to confirm.")
                return None
        print(f"There's no {item_name} here...")

    def deposit(self, item_name: str) -> None:
        """
        Deposits something the player is carrying onto the current location.
        """
        if self.world.get_location(self.x, self.y).location_number == 13 and item_name.upper() == "COIN":
            # Easter egg: If at government office and deposited coin, then automatically get tcard
            print("Ben smirked mysteriously and opened his drawer...it's your tcard! He hands it to you discreetly "
                  "and says: This never happened.")
            self.pickup_item("tcard")

        for item in self.inventory:
            if item.name.upper() == item_name.upper():
                self.world.get_location(self.x, self.y).items.append(item)
                self.inventory.remove(item)
                if self.world.get_location(self.x, self.y).location_number == item.target_position:
                    self.score += item.target_points
                    print(f"You just deposited {item.name}. You earned {item.target_points} points.")
                    return None
                print(f"You just deposited {item.name}.")
                return None
        print(f"There's no {item_name} in your inventory...")


class Puzzle:
    """
    An abstract puzzle superclass for creating different types of puzzles.

    Instance Attributes:
    - answer: the answer to the puzzle
    """
    answer: Any

    def __init__(self, answer):
        """
        Initializes a new puzzle instance. A shared method.
        """
        self.answer = answer

    def attempt_solution(self):
        """
        Attempts to solve the puzzle. This method should be implemented by subclasses.
        """
        raise NotImplementedError()


class InfiniteTriesPuzzle(Puzzle):
    """
    A Puzzle subclass where the player has infinite attempts to solve the puzzle.
    """

    def attempt_solution(self) -> bool:
        """
        Allows the player to attempt to solve the puzzle with infinite tries. Returns True when the user solves it.
        """
        user_answer = input("\nPlease enter the password: ").upper()
        while user_answer != self.answer.upper():
            print("Incorrect! Please try again.")
            user_answer = input("\nPlease enter the password: ").upper()
        print("Correct! You've solved the puzzle.")
        return True


class LimitedTriesPuzzle(Puzzle):
    """
    A Puzzle subclass where the player has a limited number of attempts to solve the puzzle.

    Extra instance attribute
    - tries: the maximum number of attempts.

    Representation Invariants:
    - tries > 0
    """
    tries: int

    def __init__(self, answer, tries):
        """
        Initializes a new instance of a limited tries puzzle.
        """
        super().__init__(answer)
        self.tries = tries

    def attempt_solution(self) -> bool:
        """
        Allows the player to attempt to solve the puzzle with a limited number of tries.
        Returns False if the player fails the puzzle.
        """
        attempts = 0
        while attempts < self.tries:
            choice = input("\nEnter your answer as a number: ")
            try:
                if int(choice) == self.answer:  # The correct answer is 2
                    print("Correct! You've got the right number.")
                    return True
                else:
                    print("Incorrect, please try again.")
                    attempts += 1
            except ValueError:
                # If the player enters a non-integer, to prevent int() from throwing ValueError
                print("Incorrect, please enter a valid number.")
                attempts += 1

            if attempts == self.tries:  # Checks if it's the last attempt
                print("Sorry, you've used all your attempts. The game will end now.")
                return False
