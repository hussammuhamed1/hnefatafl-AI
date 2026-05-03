# Hnefatafl

A simple Python implementation of the Viking board game Hnefatafl on a 9x9 board, featuring human vs AI gameplay.

## Overview

This project implements the core gameplay for Hnefatafl, including board creation, player turns, movement rules, captures, and victory conditions.

- Attackers (`A`) attempt to capture the king.
- Defenders (`D`) try to escort the king (`K`) to one of the four corner squares.
- The throne is located at the center of the board.

## Requirements

- Python 3.7+

## Installation

No external dependencies are required. Clone or download the repository, then run the game with Python.

```bash
python main.py
```

## How to Play

1. Choose whether to play as Attackers (A) or Defenders (D).
2. Select AI difficulty: easy, medium, or hard.
3. The board is printed in the console.
4. Players alternate turns starting with the attackers.
5. On your turn, enter the source row and column, then the destination row and column for your move.
6. Pieces move in straight lines along rows or columns, and cannot jump over other pieces.
7. Captures occur automatically when an enemy piece is trapped between two friendly pieces or against special squares.
8. The defenders win if the king reaches any corner square.
9. The attackers win if the king is fully surrounded and captured.

## Project Files

- `main.py` — Application entry point.
- `board.py` — Board constants, starting setup, and printing.
- `state.py` — Game state object tracking the board, current turn, and winner.
- `controller.py` — Main game loop, input handling, turn switching, and win detection.
- `moves.py` — Move validation and piece movement logic.
- `capture.py` — Capture detection, king escape, and king capture rules.
- `AI.py` — AI opponent with difficulty levels.
- `utils.py` — Helper functions for board coordinate checks.

## Notes

This is a console-based implementation intended for local play and experimentation.
