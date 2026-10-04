import matplotlib.pyplot as plt

from problem import generate_problem, SEED
from pso import PSOPathPlanner


# CALCULATE FINAL PATH LENGTH


def calculate_path_length(path):

    length = 0.0

    for i in range(len(path) - 1):

        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        distance = (
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        ) ** 0.5

        length += distance

    return length


# CHECK WHETHER THE FINAL PATH HITS AN OBSTACLE


def check_path_collision(path, obstacles):

    for point in path:

        if point in obstacles:
            return True

    return False


# =====================================================
# DISPLAY FINAL RESULT
# =====================================================

def show_result(
    grid_size,
    obstacles,
    start,
    goal,
    path
):

    plt.figure(figsize=(8, 8))

    # -----------------------------------------------
    # Draw obstacles
    # -----------------------------------------------

    for x, y in obstacles:

        plt.scatter(
            x,
            y,
            marker="s",
            s=500
        )

    # -----------------------------------------------
    # Draw PSO path
    # -----------------------------------------------

    x_values = [
        point[0]
        for point in path
    ]

    y_values = [
        point[1]
        for point in path
    ]

    plt.plot(
        x_values,
        y_values,
        marker="o",
        linewidth=2,
        markersize=4,
        label="PSO Path"
    )

    # -----------------------------------------------
    # Draw start point
    # -----------------------------------------------

    plt.scatter(
        start[0],
        start[1],
        marker="o",
        s=200,
        label="Start"
    )

    # -----------------------------------------------
    # Draw goal point
    # -----------------------------------------------

    plt.scatter(
        goal[0],
        goal[1],
        marker="*",
        s=300,
        label="Goal"
    )

    # -----------------------------------------------
    # Configure grid
    # -----------------------------------------------

    plt.xlim(-1, grid_size)
    plt.ylim(-1, grid_size)

    plt.xticks(range(grid_size))
    plt.yticks(range(grid_size))

    plt.grid(True)

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")

    plt.title(
        f"PSO 2D Path Planning\nRandom Seed = {SEED}"
    )

    plt.legend()

    # Keep X and Y scale equal
    plt.gca().set_aspect("equal")
    plt.savefig("result.png", dpi=300, bbox_inches="tight")
    plt.show()


# =====================================================
# MAIN PROGRAM
# =====================================================

def main():

    print()
    print("========================================")
    print("       PSO 2D PATH PLANNING")
    print("========================================")

    # -------------------------------------------------
    # STEP 1: Generate the unique problem
    # -------------------------------------------------

    grid_size, obstacles, start, goal = (
        generate_problem()
    )

    print("\nProblem Information")
    print("-------------------")

    print("Random Seed:", SEED)
    print(
        "Grid Size:",
        grid_size,
        "x",
        grid_size
    )

    print(
        "Number of Obstacles:",
        len(obstacles)
    )

    print("Start Point:", start)
    print("Goal Point:", goal)

    # -------------------------------------------------
    # STEP 2: Create PSO planner
    # -------------------------------------------------

    print("\nStarting PSO...")
    print("-------------------")

    planner = PSOPathPlanner(
        grid_size=grid_size,
        obstacles=obstacles,
        start=start,
        goal=goal,
        number_of_particles=40,
        number_of_waypoints=8,
        number_of_iterations=150
    )

    # -------------------------------------------------
    # STEP 3: Run PSO
    # -------------------------------------------------

    best_path, best_cost = planner.run()

    # -------------------------------------------------
    # STEP 4: Calculate final path length
    # -------------------------------------------------

    path_length = calculate_path_length(
        best_path
    )

    # -------------------------------------------------
    # STEP 5: Check final path
    # -------------------------------------------------

    has_collision = check_path_collision(
        best_path,
        obstacles
    )

    # -------------------------------------------------
    # STEP 6: Display final result
    # -------------------------------------------------

    print("\n========================================")
    print("           FINAL RESULT")
    print("========================================")

    print("\nBest Path:")

    for point in best_path:
        print(point)

    print(
        f"\nPath Length: {path_length:.2f}"
    )

    print(
        f"Best Cost: {best_cost:.2f}"
    )

    if has_collision:
        print("Path Status: Collision detected")
    else:
        print("Path Status: Obstacle-free")

    # -------------------------------------------------
    # STEP 7: Show graph
    # -------------------------------------------------

    show_result(
        grid_size,
        obstacles,
        start,
        goal,
        best_path
    )

# PROGRAM START


if __name__ == "__main__":
    main()