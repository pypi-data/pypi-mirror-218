# PyMulti (Fun) - Init

''' This is the __init__.py file. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import os
import webbrowser

# Function 1 - Game
def game(name):
    # List of Games
    games = ["ant", "bagels", "bounce", "cannon", "connect", "crypto", "fidget", "flappy", "guess", "life", "maze", "memory", "minesweeper", "pacman", "paint", "pong", "simonsays", "snake", "tictactoe", "tiles", "tron", "typing", "illusion", "tennis", "rockpaperscissors"]

    # Checking the Data Type of "name"
    if (isinstance(name, str)):
        # Checking if "name" is Valid
        if (name in games):
            # Playing the Game
            if (name in ["tennis", "rockpaperscissors"]):
                if (name == "tennis"):
                    # Opening the "Tennis" Game
                    webbrowser.open("https://anikethchavare.vercel.app/tennis-game")
                elif (name == "rockpaperscissors"):
                    # Opening the "Rock Paper Scissors" Game
                    webbrowser.open("https://anikethchavare.vercel.app/rock-paper-scissors")
            else:
                # Playing the "freegames" Game
                os.system("python -m freegames." + name)
        else:
            raise Exception("The 'name' argument must be a valid game's name. The available games are:\n\n" + str(games))
    else:
        raise TypeError("The 'name' argument must be a string.")