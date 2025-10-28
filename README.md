## Sliding Puzzle Solver

A Python implementation of a general-purpose N-Puzzle solver, capable of automatically finding optimal or near-optimal solutions to sliding puzzles (e.g., the 15-puzzle). This project explores algorithmic search strategies, heuristic optimization, and performance benchmarking on different puzzle instances.

## Algorithms

This solver uses informed search algorithms (e.g., A*) to find the minimal-move solution path.
Each state is represented as a string of tiles, and neighbor generation expands all valid moves (up, down, left, right) without revisiting previous states.

## Future Work

Implement a web-based interactive GUI

Add alternative heuristics (e.g., linear conflict)

Enable user-defined puzzles and algorithm selection
