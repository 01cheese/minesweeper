# Minesweeper

This project is a Minesweeper game built using Pygame and Pygame Menu. The game allows users to select different difficulty levels, including a custom mode where they can specify the grid size and the number of mines.

## Features

- Different difficulty levels: Easy, Medium, Hard, and Custom.
- Customizable grid size and number of mines.
- Sound effects for clicks and mine explosions.
- Game over and win conditions with congratulatory messages.

## Installation

1. Ensure you have Python installed on your system.
2. Install the required libraries:
    ```bash
    pip install pygame pygame-menu
    ```

## Running the Game

1. Save the script to a file, e.g., `minesweeper.py`.
2. Run the script:
    ```bash
    python minesweeper.py
    ```

## Code Overview

- **Imports**: The necessary libraries for the game.
- **Initialization**: Setting up Pygame, the display window, colors, fonts, and sounds.
- **Functions**:
  - `start_the_game`: Starts the game based on the selected difficulty.
  - `custom_menu`: Menu for custom game settings.
  - `show_error_menu`: Displays an error message for invalid custom settings.
  - `main_menu`: Main menu of the game.
  - `play_game`: Core game loop that handles the Minesweeper logic.
  - `show_congratulations_menu`: Displays a congratulatory message when the game is won or lost.
  
## Gameplay Instructions

1. Select the difficulty level from the main menu.
2. If `Custom Game` is selected, enter the desired grid size and number of mines.
3. Click on cells to reveal them. Right-click to flag a cell.
4. The game ends when all non-mine cells are revealed or a mine is clicked.

## File Structure

- `click.wav`: Sound file for a cell click.
- `explosion.wav`: Sound file for a mine explosion.

