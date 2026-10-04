# PSO 2D Grid Path Planning

## Student Information

- **Name:** Amna Bashir
- **Roll Number:** 059
- **Random Seed:** 59

## Project Description

This project implements Particle Swarm Optimization (PSO) to find a short and obstacle-free path from a start point to a goal point on a 2D grid.

The grid, obstacles, start point, and goal point are generated programmatically. My roll number is used as the random seed, so the problem instance is unique and reproducible.

## Problem Generation

The program generates a 20 × 20 grid and randomly places obstacles using the roll number as the random seed.

For my problem instance:

- **Grid Size:** 20 × 20
- **Number of Obstacles:** 80
- **Start Point:** (15, 0)
- **Goal Point:** (17, 12)
- **Random Seed:** 59

The start and goal points are selected only from free cells, so they are not placed on obstacles.

## PSO Approach

Particle Swarm Optimization is used to search for a good path from the start point to the goal point.

Each particle represents a possible path using intermediate waypoints. The algorithm evaluates each path using a cost function based on path distance and obstacle collisions.

A large penalty is added when a path crosses an obstacle.

During the search, each particle keeps track of its personal best position (pbest), while the swarm keeps track of the overall best position (gbest). The particles then update their velocity and position based on these best solutions.

The process continues for a fixed number of iterations, and the best path found by the swarm is selected as the final solution.

## PSO Parameters

| Parameter | Value |
|---|---:|
| Grid Size | 20 × 20 |
| Number of Obstacles | 80 |
| Number of Particles | 40 |
| Number of Waypoints | 8 |
| Number of Iterations | 150 |
| Inertia Weight (w) | 0.7 |
| Cognitive Coefficient (c1) | 1.5 |
| Social Coefficient (c2) | 1.5 |

## Final Result

The best path found by PSO was:

```text
(15, 0)
(15, 3)
(10, 8)
(9, 9)
(11, 12)
(17, 12)
Result Summary
Path Length: 21.09
Best Cost: 21.09
Path Status: Obstacle-free

Since the final path did not collide with any obstacle, no collision penalty was added to the final cost.

Visualization

The final visualization shows the generated obstacles, start point, goal point, and the best path found by PSO.

.

Project Files
File	     Purpose
problem.py	Generates the grid, obstacles, start point, and goal point
pso.py	    Implements the PSO path-planning algorithm
main.py	    Runs the complete program and displays the result
requirements.txt	Contains the required Python package
flow_diagram.jpg	Hand-drawn algorithm flow diagram
result.png	        Final PSO path visualization
How to Run

Install the required package:

pip install -r requirements.txt

Then run:

python main.py

The program will generate the problem, run PSO, print the best path and its cost, and display the final path.

Technologies Used
Python
Particle Swarm Optimization (PSO)
Matplotlib
Git
GitHub