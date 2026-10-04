import random

ROLL_NUMBER = 59       

# Roll number is used as the random seed
SEED = ROLL_NUMBER


# GRID SETTINGS

GRID_SIZE = 20

# 20% of the grid will contain obstacles
OBSTACLE_PERCENTAGE = 0.20


def generate_problem():

    # Use roll number as the random seed
    random.seed(SEED)

    # Create all cells of the grid
    all_cells = [
        (x, y)
        for x in range(GRID_SIZE)
        for y in range(GRID_SIZE)
    ]

    # Calculate number of obstacles
    obstacle_count = int(
        GRID_SIZE * GRID_SIZE * OBSTACLE_PERCENTAGE
    )

    # Randomly select obstacle cells
    obstacles = set(
        random.sample(all_cells, obstacle_count)
    )

    # Find cells that are not obstacles
    free_cells = [
        cell
        for cell in all_cells
        if cell not in obstacles
    ]

    # Randomly select start point
    start = random.choice(free_cells)

    # Select goal from another free cell
    remaining_cells = [
        cell
        for cell in free_cells
        if cell != start
    ]

    goal = random.choice(remaining_cells)

    return GRID_SIZE, obstacles, start, goal


# TEST THE PROBLEM GENERATION

if __name__ == "__main__":

    grid_size, obstacles, start, goal = generate_problem()

   
    print("GENERATED PROBLEM")
    print("Random Seed:", SEED)
    print("Grid Size:", grid_size, "x", grid_size)
    print("Number of Obstacles:", len(obstacles))
    print("Start Point:", start)
    print("Goal Point:", goal)

    print("\nObstacle Cells:")
    print(sorted(obstacles))