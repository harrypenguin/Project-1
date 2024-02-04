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
from typing import Optional, TextIO


class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - position: the position of the location in the world map
        - brief_description: a brief description of the location
        - long_description: a detailed description of the location
        - actions: a list of actions available at this location
        - items: a list of the items available at this location
        - visited_before: whether this location has been visited before

    Representation Invariants:
        - TODO: add representation invariants
    """
    position: list[int, int]
    score: int
    brief_description: str
    long_description: str
    actions: list[str]
    items: list[Item]
    visited_before: bool

    def __init__(self, position: list[int, int], score: int, brief_description: str, long_description: str,
                 actions: list[str], items: list[Item], visited_before: bool) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        self.position = position
        self.score = score
        self.brief_description = brief_description
        self.long_description = long_description
        self.actions = actions
        self.items = items
        self.visited_before = visited_before

    def available_actions(self):
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed

        # TODO: Complete this method, if you'd like or remove/replace it if you're not using it -- I don't think we need this bc the World method already does this

    def get_coordinates(self, map_data: TextIO) -> list[int, int]:
        """
        Return the x, y coordinates of the Location based on map.txt. map_data is an open text file.
        """

    def get_items(self, items_data: TextIO) -> list[Item]:
        """
        Return a list of Item objects currently at this location.
        """


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TODO

    Representation Invariants:
        - # TODO
    """

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


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - # TODO

    Representation Invariants:
        - # TODO
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - locations: a dictionary mapping location numbers to Location objects
        - items: a list of Item objects

    Representation Invariants:
        - # TODO
    """

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
            line = line.strip('\n').split(' ')
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
        TODO: Should we have scores for each location? List of possible actions?
        """

        location_loaded = []
        lines = location_data.readlines()
        for i in range(len(lines)):
            if lines[i][0:8] == "LOCATION":
                location_number = int(lines[i][9:len(lines[i])].strip("\n"))
                score = int(lines[i + 1].strip("\n"))
                short_description = lines[i + 2].strip("\n")
                long_description = lines[i + 3].strip("\n")
                actions = []
                j = i + 4
                while lines[j] != "END":
                    actions += lines[j]
                    j += 1

                coordinates = [0, 0]
                for x in self.map:
                    for y in x:
                        if y == location_number:
                            coordinates = [self.map.index(x), x.index(y)]

                location_loaded[location_number] = Location(coordinates, score, short_description, long_description,
                                                            actions, [], False)
        return location_loaded

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)
        """

        location_number = self.map[x][y]
        return self.locations[location_number]
