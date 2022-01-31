# Ranking League Table calculator [![Actions Status: Python application](https://github.com/gerhardkeuck/game_ranking/workflows/Python%20application/badge.svg)](https://github.com/gerhardkeuck/game_ranking/actions?query=workflow%3A"Python+application")

Demo project for solving the game ranking table problem.

Given an input game results table, output the sorted list of team ranks.

The points are allocated using the following rules:
- On ties, each team receives 1 points.
- On win, team gets 3 points.
- On loss, team gets 0 points.

## Requirements
The application requires Python 3 (was tested against 3.10).

The `python` cli executable should map to Python 3 and not to Python 2.

## How to use the application


Execute the `main.py` module with a file path as argument. The sorted ranking
will be the output.

Example:
```
python main.py ./test/data/example_problem.txt
```

Example input (from `example_problem.txt`):
```
Lions 3, Snakes 3
Tarantulas 1, FC Awesome 0
Lions 1, FC Awesome 1
Tarantulas 3, Snakes 1
Lions 4, Grouches 0
```
Expected output (from `example_solution.txt`):
```
1. Tarantulas, 6 pts
2. Lions, 5 pts
3. FC Awesome, 1 pt
3. Snakes, 1 pt
5. Grouches, 0 pts
```

## Executing tests

Tests can be executed with the following command:
```
python -m unittest discover test
```
