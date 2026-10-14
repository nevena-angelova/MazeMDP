import matplotlib.pyplot as plt
import numpy as np

ROWS, COLS = 5, 6
ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
MOVE_REWARD = -1
OBSTACLE_REWARD = -100
GOAL_REWARD = 100
DISCOUNT = 0.9
THETA = 0.01
MAX_ITER = 50

# Maze representation
# 0 = free space, 1 = obstacle, 4,5 = goal
maze_map = [
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0]
]

# Transform values into MDP
maze = [[OBSTACLE_REWARD if cell == 1 else 0 for cell in row] for row in maze_map]
maze[4][5] = GOAL_REWARD

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def is_obstacle(r, c):
    return maze[r][c] == OBSTACLE_REWARD

def next_state(r, c, action):
    dr, dc = ACTIONS[action]
    nr, nc = r + dr, c + dc
    if in_bounds(nr, nc) and not is_obstacle(nr, nc):
        return nr, nc
    return r, c

def value_iteration():
    V = [[0]*COLS for _ in range(ROWS)]
    policy = [['']*COLS for _ in range(ROWS)]

    for _ in range(MAX_ITER):
        delta = 0
        new_V = [[0]*COLS for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                if maze[r][c] == OBSTACLE_REWARD or maze[r][c] == GOAL_REWARD:
                    new_V[r][c] = maze[r][c]
                    continue
                best, best_action = float('-inf'), ''
                for a in ACTIONS.keys():
                    nr, nc = next_state(r, c, a)
                    reward = MOVE_REWARD
                    value = reward + DISCOUNT * V[nr][nc]
                    if value > best:
                        best, best_action = value, a
                new_V[r][c] = best
                policy[r][c] = best_action
                delta = max(delta, abs(V[r][c] - best))
        V = new_V
        if delta < THETA:
            break
    return policy

def extract_path(policy):
    r, c = 0, 0
    path = [(r, c)]
    while (r, c) != (4, 5):
        a = policy[r][c]
        if not a:
            print("No path to goal found.")
            return path
        r, c = next_state(r, c, a)
        if (r, c) in path:
            print("Loop detected in path extraction.")
            return path
        path.append((r, c))
    return path

# Start
policy = value_iteration()
path = extract_path(policy)

print(policy)
print(path)


# Visualization function
def visualize_maze(maze, path, start, goal, title):
    maze_np = np.array(maze)

    fig, ax = plt.subplots()
    ax.imshow(maze_np, cmap='Greys')
    path.insert(0, (start[0], start[1]))
    px, py = zip(*path)
    ax.plot(py, px, color='red', linewidth=2, label='Path')

    ax.scatter(start[1], start[0], marker='o', color='green', s=100, label='Start')
    ax.scatter(goal[1], goal[0], marker='X', color='blue', s=100, label='Goal')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend()
    ax.set_title(title)
    plt.show()


visualize_maze(maze, path, (0, 0), (4, 5), "Maze Path Visualization")