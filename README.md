# OptimizationProblemSolver

This project addresses two main optimization problems:

## Problem 1: Task Allocation Optimization

Description: Assign  tasks to  nodes while minimizing total costs, including task execution and node activation costs. Constraints include node capacities, task requirements, and node activation.

Solution: A Mixed-Integer Linear Programming (MILP) model was implemented using Gurobi Optimizer. Decision variables determine task assignments and node activations. Constraints ensure resource feasibility and optimal task distribution. The objective function minimizes the sum of task and activation costs.

## Problem 2: Resource Allocation Optimization

Description: Allocate resources to elements, balancing benefit and cost. Each element's allocation impacts total benefit and cost, modeled by a linear cost function.

Solution: A Linear Programming (LP) model was developed to maximize net benefit. Decision variables represent allocated resource proportions. The objective function optimizes the trade-off between benefit and increasing costs.

Key Features

Flask-based web interface for user input and visualization.

Gurobi-based optimization for scalable and efficient problem-solving.

Clear visual representation of results through dynamic graphs and tables.
