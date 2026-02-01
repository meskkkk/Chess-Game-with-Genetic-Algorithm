# Chess Game with Genetic Algorithm AI

An interactive chess game built with Python that features a GUI powered by customtkinter and an AI opponent that uses genetic algorithms to make intelligent moves.

## Features

- **Interactive GUI**: Play chess with a clean, user-friendly interface built with customtkinter
- **AI Opponent**: Black pieces are controlled by an intelligent AI using genetic algorithm optimization
- **Move Validation**: Enforces standard chess rules using the python-chess library
- **Check Detection**: Highlights the king when in check
- **Game Status**: Detects checkmate and stalemate conditions
- **Visual Feedback**:
  - Green highlights for valid moves
  - Pink highlights for capture moves
  - Red highlights for kings in check

## Requirements

- Python 3.x
- customtkinter
- python-chess
- Pillow (PIL)

## Installation

1. Install required dependencies:

```bash
pip install customtkinter python-chess pillow
```

2. Ensure you have the necessary asset files in the project directory:
   - Chess piece images (white_pawn.png, black_king.png, etc.)
   - Chess wallpaper (Chess Wallpaper.jpeg)
   - Chess logo (chess.png)

## How to Run

```bash
python Chess.py
```

## Gameplay

1. **Main Menu**: Start by selecting "Play" to begin a new game
2. **Player Controls**: Click on a white piece to select it, then click on a valid destination to move
3. **AI Moves**: After your move, the black AI automatically makes its move
4. **Game End**: The game ends when checkmate or stalemate is reached

## Technical Details

### Genetic Algorithm AI

The AI uses a genetic algorithm to evaluate move sequences:

- **Population**: Generates random move sequences
- **Fitness Evaluation**: Scores moves based on:
  - Material value (pieces captured/controlled)
  - Piece safety (attack vulnerability)
  - Center control (board position dominance)
  - King safety (invaluable piece)
- **Selection**: Keeps the top 50% of sequences (elitism)
- **Crossover**: Creates new sequences by combining parent sequences
- **Mutation**: Randomly alters sequences with configurable probability
- **Iterations**: Evolves over multiple generations to find optimal moves

### Class Structure

- **GeneticAlgorithm**: Implements the genetic algorithm for move evaluation
- **ChessGUI**: Manages the graphical interface and game flow

## File Structure

```
Chess.py                    # Main application file
Chess.iml                   # IntelliJ IDEA project file
README.md                   # This file
```

## Controls

- **Click on a piece**: Select a piece to move
- **Click on a destination**: Move the selected piece
- **Valid moves**: Shown in green
- **Capture moves**: Shown in pink
- **King in check**: Highlighted in red

## Notes

- White pieces are player-controlled
- Black pieces are AI-controlled using the genetic algorithm
- The algorithm adapts its strategy based on board evaluation
- Game rules follow standard chess conventions
