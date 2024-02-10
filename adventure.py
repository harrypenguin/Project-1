"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
import random

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player


def caesar_cipher(text: str) -> str:
    """
    Takes in a string and converts it into ciphertext with the caesar cipher encryption algorithm. The shift is random
    each time. Used to generate the hint for Gerstein basement's password.
    """
    encrypted_text = ""
    shift = random.randint(1, 25)
    for char in text:
        shift_amount = shift % 26
        if char.isalpha():
            if char.islower():
                new_char = chr((ord(char) - 97 + shift_amount) % 26 + 97)
            else:
                new_char = chr((ord(char) - 65 + shift_amount) % 26 + 65)
            encrypted_text += new_char
        else:
            encrypted_text += char
    return encrypted_text


# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(2, 5, w)  # set starting location of player; you may change the x, y coordinates here as appropriate

    while not p.victory:
        location = w.get_location(p.x, p.y)

        if p.moves <= 0:
            print("You ran out of moves! The game is over.")
            # End the game if the player runs out of moves.
            exit()

        items_here = [item.name for item in location.items]
        if location.location_number == 14 and all([item in items_here for item in ['Cheat sheet', 'Pen', 'Tcard']]):
            print("You successfully collected all the items for the exam. The doors open and you walk in...")
            print(f"Game over. Your final score is {p.score}")
            # The player wins when all required items are brought to exam centre.
            p.victory = True

        if location.visited_before:
            print(location.brief_description)
        else:
            print(location.long_description)

        if location.items:
            print("Items available here: ")
            for item in location.items:
                print(item.name)

        if location.location_number == 3:
            toms_message = ('Hello! I am Tom Fairgrieve, I taught CSC110. '
                            'If you learned Caesar Cipher, you would know the password is Tom Fairgrieve!')

            print(f"Professor Fairgrieve seems to be talking to himself. You can't exactly make out what he's saying. "
                  f"It just sounds like mumbling! \nAs you get closer, you realize his speech is completely slurred: "
                  f"\n'{caesar_cipher(toms_message)}...' What?? Is your hearing ok??")
            # Generate and print cipher hint for Gerstein basement password

        if location.location_number == 8 and not location.visited_before:
            # Elevator puzzle
            # TODO: Play pitch here -- or maybe make random generation each time?

            for i in range(3):  # Gives the player 3 attempts
                choice = input("\nEnter your answer as a number: ")
                try:
                    if int(choice) == 2:  # The correct answer is 2
                        print("Correct! You've got the right number.")
                        p.x = 6
                        p.y = 5
                        break
                    else:
                        print("Incorrect, please try again.")
                except ValueError:
                    # If the player enters a non-integer, to prevent int() from throwing ValueError
                    print("Incorrect, please enter a valid number.")

                if i == 2:  # Checks if it's the last attempt
                    print("Sorry, you've used all your attempts. The game will end now.")
                    # TODO: End?? Maybe don't end if u have engineer hat or smt
                    exit()
        elif location.location_number == 7 and not location.visited_before:
            # Bookshelf puzzle
            choice = input("\nPlease enter the passcode to open the bookshelf:")
            while choice.upper() != "TOM FAIRGRIEVE":
                print("Incorrect! Please try again.")
                choice = input("\nPlease enter the passcode to open the bookshelf:")
            print("The bookshelf has been opened!")
            location.visited_before = True
        elif location.location_number == 12 and not location.visited_before:
            if any([item.name == "Construction hat" for item in p.inventory]):
                print("Good thing you have a hard hat...The fall did no damage. Don't fall in again!")
            else:
                p.moves -= 3
                print("Ouch! You just lost 3 moves...don't the engineers have construction hats to protect themselves?")
        else:
            print("What to do? \n")
            print("[menu]")
            for action in location.available_actions():
                print(action)
            choice = input("\nEnter action: ")

            if choice == "[menu]":
                print("Menu Options: \n")
                for option in location.available_actions():
                    print(option)
                choice = input("\nChoose action: ")

            if "GO " in choice.upper():
                p.move(choice[3:])

            if "PICKUP " in choice.upper():
                if location.location_number == 13:
                    print("Ben vehemently denies that he is in possession of your tcard...although it's right there!")
                    # Prevents the player from directly picking up the tcard at parliament. The deposit command
                    # will allow automatic pickup if Ben is bribed.
                    continue
                p.pickup_item(choice[7:])

            if "DEPOSIT " in choice.upper():
                p.deposit(choice[8:])

            if choice.upper() == "LOOK":
                print(location.long_description)

            if choice.upper() == "INVENTORY":
                p.check_inventory()

            if choice.upper() == "SCORE":
                p.get_score()

            if choice.upper() == "QUIT":
                yes_or_no = input("Are you sure you want to end the game? Y/N")
                if yes_or_no == "Y":
                    exit()
                else:
                    continue

        if not location.visited_before:
            location.visited_before = True


        # TODO: CALL A FUNCTION HERE TO HANDLE WHAT HAPPENS UPON THE PLAYER'S CHOICE
        #  REMEMBER: the location = w.get_location(p.x, p.y) at the top of this loop will update the location if
        #  the choice the player made was just a movement, so only updating player's position is enough to change the
        #  location to the next appropriate location
        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
