# Fruit Slicer

**Fruit Slicer** is a fast-paced arcade game where your keyboard is your weapon! Slice fruits by typing the corresponding letters, avoid bombs, and freeze time with special power-ups. Challenge yourself in Classic Mode or face off against a friend in Versus Mode.

## Features

- **Classic Mode**: Test your reflexes and typing speed. Slice as many fruits as possible without dropping them or hitting bombs.
- **Versus Mode**: A local 1v1 multiplayer mode. Compete to see who can get the highest score in 60 seconds.
- **Special Fruits**:
  - **Bomb**: Don't type this letter! Hitting a bomb costs you 3 lives.
  - **Ice**: Freezes time and slows down fruit spawning for a short duration.
- **Leaderboard**: Track your high scores and compete for the top spot.

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- `pygame-ce` (Community Edition)
- `moviepy`

## Installation

1. Clone the repository or download the source code.
2. Open a terminal in the project directory.
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## How to Play

Run the game using Python:

```bash
python main.py
```

### Controls

#### Classic Mode
Type the letter displayed on the falling fruit to slice it.
- **Possible Letters**: A, Z, E, R, U, I, O, P

#### Versus Mode (1v1)
Two players share the keyboard.
- **Player 1 (Left)**: A, Z, E, R
- **Player 2 (Right)**: U, I, O, P

## Project Structure

- `main.py`: Entry point of the game.
- `src/`: Contains the source code for the game logic, entities, and UI.
- `data/`: Stores game data like leaderboards.
- `assets/`: Contains images and sounds.

---
*Created by Nathan, Haïk and Elyes*
