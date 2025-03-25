# Sokoban Game with Tkinter GUI - README

This project implements a Sokoban game using Python's Tkinter library. The game presents a series of puzzles where the player must push boxes to their target locations within a grid. The game includes three levels of increasing difficulty, each with its own unique layout and challenges. The user can play manually or use an automated solver to complete the levels.

## Table of Contents
1. [Overview](#overview)
2. [Game Features](#game-features)
3. [Setup Instructions](#setup-instructions)
4. [Game Controls](#game-controls)
5. [How It Works](#how-it-works)
6. [Credits](#credits)

---

## Overview

The game is based on the classic Sokoban puzzle where the objective is to push boxes into goal positions without blocking yourself from completing the puzzle. The player can move in four directions (up, down, left, right) and push boxes into empty spaces or goals. If the player successfully positions all boxes on their goals, they win the level.

### Key Features:
- Three levels with different grid layouts.
- Grid is displayed with walls (O), player (P), boxes (B), goals (G), and boxes on goals (GB).
- Ability to reset the game to its initial state.
- Automatic solver using a breadth-first search (BFS) algorithm.
- Visual feedback with images for walls, player, boxes, and goals.
- Win condition that displays a message box when the level is completed.

---

## Game Features

- *Levels*: The game includes three different levels, each with a unique layout and increasing difficulty.
- *Manual Play*: Players can move the player character (P) and push boxes (B) manually within the game grid.
- *Automatic Solver*: A BFS-based solver that automatically determines a solution path and moves the player along the path.
- *Reset Feature*: Players can reset the game back to its initial state.
- *Win Condition*: The game checks if all boxes are placed on the correct goal positions, and displays a message when the player wins.

---

## Setup Instructions

### Requirements:
- Python 3.6 or higher
- Tkinter (usually pre-installed with Python)
- Images for the game elements (walls, player, boxes, goals). Make sure the image paths are correct or change them in the code.

### Dependencies:
- tkinter: For the graphical user interface (GUI).
- collections: For managing queues in the BFS algorithm.

### Steps to Run:

1. *Download the Game*: Clone or download the Sokoban game files to your local machine.
2. *Add Images*: The game relies on image files for the walls, player, boxes, and goals. Ensure that you have the following image files available:
    - wall.png: Wall image for obstacles.
    - playerD.png: Image of the player character.
    - box.png: Image of the box.
    - target.png: Image of the goal.
    - valid_box.png: Image of a box placed on the goal.

    Update the paths in the code to match where the images are stored on your system.

3. *Run the Game*: Open a terminal or command prompt and navigate to the folder where the game files are located. Run the following command:
   bash
   python sokoban_game.py
   

4. *Play*: The game will open a window where you can select which level to start with. After selecting a level, you can begin playing the game.

---

## Game Controls

- *Arrow Keys*: Use the arrow keys to move the player (P) in the grid. The player can move up, down, left, or right.
- *Push Boxes*: To move a box (B), the player must push it into an empty space or onto a goal (G).
- *Automatic Solver*: Click the "Start" button to allow the automatic solver to solve the level. The solution path will be followed step by step.

---

## How It Works

### 1. *Grid Layouts*:
   The game uses different grids for each level:
   - *Level 1*: A relatively simple grid with walls and boxes.
   - *Level 2*: A more challenging layout with fewer empty spaces and more obstacles.
   - *Level 3*: The hardest level, featuring many boxes and a complex arrangement of walls and goals.

### 2. *Game State*:
   The game state is represented by a grid of characters:
   - 'O': Wall
   - 'P': Player
   - 'B': Box
   - 'G': Goal
   - 'GB': Box on Goal

   Each time the player moves, the grid is updated, and the canvas is redrawn to reflect the new state.

### 3. *Movement Logic*:
   The player can move in any direction unless blocked by a wall (O) or another box (B). If the player moves onto a box, the box will be pushed if there is an empty space or goal (G) to push it into.

### 4. *Solver*:
   The BFS-based solver searches for a valid sequence of moves to solve the puzzle. It checks for all possible movements and uses a queue to explore them efficiently. If a solution is found, the sequence of moves is displayed in the console and the solver automatically solves the puzzle by following the calculated path.

### 5. *Win Condition*:
   Once all boxes are placed on goal positions (GB), the player wins the level, and a message box is displayed. The game then closes, and the level selection window appears for the player to choose the next level.

---
