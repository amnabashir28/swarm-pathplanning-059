import random
import math

# PARTICLE


class Particle:

    def __init__(self, number_of_waypoints, grid_size):

        self.number_of_waypoints = number_of_waypoints
        self.grid_size = grid_size

        # Each particle represents one possible path.
        # The path contains some intermediate waypoints.
        self.position = []

        # Velocity tells us how the waypoints will move.
        self.velocity = []

        for _ in range(number_of_waypoints):

            x = random.uniform(0, grid_size - 1)
            y = random.uniform(0, grid_size - 1)

            self.position.append([x, y])

            self.velocity.append([
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            ])

        # Initially, the current position is the
        # particle's personal best.
        self.best_position = [
            point[:] for point in self.position
        ]

        self.best_cost = float("inf")


# =====================================================
# PSO PATH PLANNER
# =====================================================

class PSOPathPlanner:

    def __init__(
        self,
        grid_size,
        obstacles,
        start,
        goal,
        number_of_particles=40,
        number_of_waypoints=8,
        number_of_iterations=150
    ):

        self.grid_size = grid_size
        self.obstacles = obstacles
        self.start = start
        self.goal = goal

        self.number_of_particles = number_of_particles
        self.number_of_waypoints = number_of_waypoints
        self.number_of_iterations = number_of_iterations

        # PSO parameters
        self.w = 0.7
        self.c1 = 1.5
        self.c2 = 1.5

        # Create the swarm
        self.particles = [
            Particle(
                number_of_waypoints,
                grid_size
            )
            for _ in range(number_of_particles)
        ]

        # Global best solution
        self.global_best_position = None
        self.global_best_cost = float("inf")

    # =================================================
    # DISTANCE BETWEEN TWO POINTS
    # =================================================

    def distance(self, point1, point2):

        return math.sqrt(
            (point1[0] - point2[0]) ** 2 +
            (point1[1] - point2[1]) ** 2
        )

    # CONVERT WAYPOINT TO GRID CELL
    

    def convert_to_cell(self, point):

        x = int(round(point[0]))
        y = int(round(point[1]))

        # Make sure the point stays inside the grid
        x = max(0, min(self.grid_size - 1, x))
        y = max(0, min(self.grid_size - 1, y))

        return (x, y)

    
    # FIND CELLS BETWEEN TWO POINTS
  

    def line_cells(self, start, end):

        x1, y1 = start
        x2, y2 = end

        cells = []

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1

        error = dx - dy

        while True:

            cells.append((x1, y1))

            if x1 == x2 and y1 == y2:
                break

            double_error = 2 * error

            if double_error > -dy:
                error -= dy
                x1 += sx

            if double_error < dx:
                error += dx
                y1 += sy

        return cells

    
    # CREATE COMPLETE PATH
    

    def create_path(self, position):

        # Start with the actual start point
        path = [self.start]

        # Add the particle's intermediate waypoints
        for point in position:

            path.append(
                self.convert_to_cell(point)
            )

        # Finish at the goal
        path.append(self.goal)

        # Remove consecutive duplicate cells
        cleaned_path = [path[0]]

        for point in path[1:]:

            if point != cleaned_path[-1]:
                cleaned_path.append(point)

        return cleaned_path


    # CALCULATE PATH COST
    

    def calculate_cost(self, position):

        path = self.create_path(position)

        total_distance = 0
        collision_count = 0

        # Check every section of the path
        for i in range(len(path) - 1):

            current_point = path[i]
            next_point = path[i + 1]

            # Calculate distance
            total_distance += self.distance(
                current_point,
                next_point
            )

            # Find cells between the two points
            cells = self.line_cells(
                current_point,
                next_point
            )

            # Check for obstacles
            for cell in cells:

                if cell in self.obstacles:
                    collision_count += 1

        # Large penalty for hitting obstacles
        collision_penalty = collision_count * 1000

        total_cost = (
            total_distance +
            collision_penalty
        )

        return total_cost

    
    # UPDATE PARTICLE
  

    def update_particle(self, particle):

        for i in range(self.number_of_waypoints):

            for dimension in range(2):

                r1 = random.random()
                r2 = random.random()

                # Cognitive component:
                # Move toward the particle's own best position
                cognitive = (
                    self.c1
                    * r1
                    * (
                        particle.best_position[i][dimension]
                        - particle.position[i][dimension]
                    )
                )

                # Social component:
                # Move toward the swarm's best position
                social = (
                    self.c2
                    * r2
                    * (
                        self.global_best_position[i][dimension]
                        - particle.position[i][dimension]
                    )
                )

                # Update velocity
                particle.velocity[i][dimension] = (
                    self.w
                    * particle.velocity[i][dimension]
                    + cognitive
                    + social
                )

                # Update position
                particle.position[i][dimension] += (
                    particle.velocity[i][dimension]
                )

                # Keep the waypoint inside the grid
                particle.position[i][dimension] = max(
                    0,
                    min(
                        self.grid_size - 1,
                        particle.position[i][dimension]
                    )
                )

    
    # RUN PSO

    def run(self):

        for iteration in range(
            self.number_of_iterations
        ):

            # Evaluate every particle
            for particle in self.particles:

                cost = self.calculate_cost(
                    particle.position
                )

                # Update personal best
                if cost < particle.best_cost:

                    particle.best_cost = cost

                    particle.best_position = [
                        point[:]
                        for point in particle.position
                    ]

                # Update global best
                if cost < self.global_best_cost:

                    self.global_best_cost = cost

                    self.global_best_position = [
                        point[:]
                        for point in particle.position
                    ]

            # Move all particles
            for particle in self.particles:

                self.update_particle(particle)

            # Show progress every 10 iterations
            if (iteration + 1) % 10 == 0:

                print(
                    f"Iteration {iteration + 1}: "
                    f"Best Cost = "
                    f"{self.global_best_cost:.2f}"
                )

        # Convert the best solution into a complete path
        best_path = self.create_path(
            self.global_best_position
        )

        return best_path, self.global_best_cost