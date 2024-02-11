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
import pygame

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player, Puzzle, InfiniteTriesPuzzle, LimitedTriesPuzzle


def play_sound(file_path):
    """
    Puzzle helper function to play a certain pitch.
    """
    # Initialize the pygame mixer
    pygame.mixer.init()
    # Load the sound file
    sound = pygame.mixer.Sound(file_path)
    # Play the sound
    sound.play()


def caesar_cipher(text: str) -> str:
    """
    Puzzle helper function.
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
            # If there are items here, display them.
            print("Items available here: ")
            for item in location.items:
                print(item.name)

        if location.location_number == 3:
            # Special interaction with Tom
            toms_message = ('Hello! I am Tom Fairgrieve, I taught CSC110. '
                            'If you learned Caesar Cipher, you would know the password is Tom Fairgrieve!')

            # Generate and print cipher hint for Gerstein basement password
            print(f"Professor Fairgrieve seems to be talking to himself. You can't exactly make out what he's saying. "
                  f"It just sounds like mumbling! \nAs you get closer, you realize his speech is completely slurred: "
                  f"\n'{caesar_cipher(toms_message)}...' What?? Is your hearing ok??")

        if location.location_number == 8 and not location.visited_before:
            # Elevator puzzle
            play_sound("pitch.mp3")

            elevator_puzzle = LimitedTriesPuzzle(2, 3)
            if elevator_puzzle.attempt_solution():
                p.x = 6
                p.y = 5
            else:
                exit()

        elif location.location_number == 7 and not location.visited_before:
            # Bookshelf puzzle
            cipher_puzzle = InfiniteTriesPuzzle('Tom Fairgrieve')
            if cipher_puzzle.attempt_solution():
                print("The bookshelf has been opened!")
                location.visited_before = True

        elif location.location_number == 12 and not location.visited_before:
            # Construction trap!
            if any([item.name == "Construction hat" for item in p.inventory]):
                # If the construction hat item is in the inventory, the player does not lose moves.
                print("Good thing you have a hard hat...The fall did no damage. Don't fall in again!")
            else:
                p.moves -= 3
                print("Ouch! You just lost 3 moves...don't the engineers have construction hats to protect themselves?")

        else:
            # Normal prompts for when there are no special features
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
                    # Skip to the next game cycle

        if not location.visited_before:
            # Makes sure the location is marked as visited before, if not already.
            location.visited_before = True


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
