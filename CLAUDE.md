# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

University assignment (DSCM046 Artificial Intelligence, Assignment 3): find the shortest path through a 5×6 grid maze from (0,0) to (4,5) by modelling it as a Markov Decision Process and solving it with value iteration. `Assignment3-Nevena-Angelova.pdf` is the written report describing the approach; `animation.gif` is a visual asset. Keep the code consistent with what the report describes (rewards, γ, θ, iteration cap, function names) or update both together.

## Running

```bash
python3 maze.py
```

Requires `numpy` and `matplotlib` (no requirements file). The script prints the policy matrix and the path, then opens a blocking matplotlib window. There are no tests, linter config, or build step.

## Architecture (`maze.py`, single script, runs at import)

- `maze_map` is the human-editable grid (0 = free, 1 = obstacle). It is converted into `maze`, a reward grid: obstacles become `OBSTACLE_REWARD` (-100) and the goal cell `maze[4][5]` is set to `GOAL_REWARD` (100). Cell values in `maze` double as type markers — `is_obstacle` and `value_iteration` identify obstacles/goal by comparing against these reward constants, so changing a constant changes classification too.
- Transitions are deterministic: `next_state` returns the current cell when a move would hit a wall or obstacle, so obstacle cells are never actually entered (their -100 is a fixed value, not a penalty that is ever collected). Every move costs `MOVE_REWARD` (-1).
- `value_iteration()` does synchronous Bellman updates (`new_V` from old `V`) for up to `MAX_ITER` sweeps or until max delta < `THETA`; obstacle and goal cells are pinned to their reward values. It returns only the greedy policy (action letters `U/D/L/R`), not the value grid.
- `extract_path()` follows the policy from the start, stopping on an empty action or a revisited cell (loop guard).
- `visualize_maze()` plots the reward grid with the path overlaid; note it mutates `path` by inserting the start again at index 0.

The start (0,0) and goal (4,5) are hardcoded in several places (`maze[4][5]`, `extract_path`, the final `visualize_maze` call) and `ROWS`/`COLS` must match `maze_map` — change all of them together when altering the maze.
