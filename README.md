# rl_tictactoe
Learning to train a tic-tac-toe model through gameplay with clean visualization.


## Files Overview

### Core Game Environment
* `t3.py` - TicTacToe game class with board logic and move validation
* `display.py` - Clean board visualization with in-place updates
* `display_config.py` - Configuration settings for different display modes
* `main.py` - Updated to use the new display system
* `example_usage.py` - Comprehensive examples of display system usage
* `moves.py`: Defines move generators for test games (predefined and random), including scenarios for X win, O win, draw, and randomized move sequences.

### Quick Start
```bash
uv sync
uv run main.py # for the computer to play random moves as both X and O
uv run playHuman.py # computer is random, user is other player
```
